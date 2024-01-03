# SPDX-FileCopyrightText: 2023 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-2.0-only

import multiprocessing
import multiprocessing.pool
import threading
import time
import enum

from photoassistant.utils.descriptors import RDescriptor
from photoassistant.utils.descriptors import RWDescriptor
from photoassistant.utils.processingutils import AsyncExecutePolicy


class AsyncSharedCacheQueryPolicy:
    NONE = object()
    query_owner = RDescriptor()
    function = RDescriptor()
    callback = RDescriptor()
    result_placeholder = RWDescriptor()

    def __init__(self, query_owner, function, callback=None):
        self._query_owner = query_owner
        self._function = function
        self._callback = callback
        self._result_placeholder = AsyncSharedCacheQueryPolicy.NONE

    def get_query_owner(self):
        return self._query_owner

    def get_function(self):
        return self._function

    def get_callback(self):
        return self._callback

    def get_result_placeholder(self):
        return self._result_placeholder

    def set_result_placeholder(self, value):
        self._result_placeholder = value

    def delete_result_placeholder(self):
        self._result_placeholder = AsyncSharedCacheQueryPolicy.NONE


class CacheObject:
    data = RWDescriptor()
    last_access = RDescriptor()
    touched = RDescriptor()

    def __init__(self):
        self._data = None
        self._touched = threading.Event()
        self._ready = threading.Event()
        self._last_access = time.time()
        self.cache_object_lock = threading.Lock()

    def get_data(self):
        with self.cache_object_lock:
            self._touched.set()
            self._last_access = time.time()
            return self._data

    def set_data(self, data):
        with self.cache_object_lock:
            self._touched.set()
            self._last_access = time.time()
            self._data = data
            self._ready.set()

    def get_last_access(self):
        with self.cache_object_lock:
            return self._last_access

    def get_touched(self):
        return self._touched.is_set()

    def wait(self):
        return self._ready.wait()

    def is_ready(self):
        return self._ready.is_set()

    def touch(self):
        with self.cache_object_lock:
            self._touched.set()
            self._last_access = time.time()


class CacheState(enum.IntEnum):
    DATA_READY = 0
    DATA_MISSING = 1
    DATA_WAITING = 2


class SizeRestrictedCache:
    DELETE_THREAD_SLEEP_1 = 0.01
    DELETE_THREAD_SLEEP_2 = 0.5

    def __init__(self, slots):
        self.slots = slots
        self._cache = dict()
        self._cache_lock = threading.RLock()

        self._delete_old_cache_objects_worker_thread_lock = threading.Lock()
        self._delete_old_cache_objects_worker_thread = None

    def __len__(self):
        with self._cache_lock:
            return sum(sum(len(owner_function_cache) for owner_function_cache in owner_cache.values()) for owner_cache in self._cache.values())

    def get_cache_state(self, cache_owner, cache_function, key):
        with self._cache_lock:
            owner_cache = self._cache.get(cache_owner, dict())
            owner_function_cache = owner_cache.get(cache_function, dict())
            cache_object = owner_function_cache.get(key, None)
            if cache_object is None:
                return CacheState.DATA_MISSING
            if cache_object.is_ready():
                return CacheState.DATA_READY
            else:
                return CacheState.DATA_WAITING

    def query_cache_object(self, cache_owner, cache_function, key):
        with self._cache_lock:
            owner_cache = self._cache.get(cache_owner, dict())
            owner_function_cache = owner_cache.get(cache_function, dict())
            cache_object = owner_function_cache.get(key, CacheObject())
            owner_function_cache[key] = cache_object
            owner_cache[cache_function] = owner_function_cache
            self._cache[cache_owner] = owner_cache

            self._delete_old_cache_objects_in_separate_thread()

        return cache_object

    def _delete_old_cache_objects_loop(self):
        # The reference 'self._delete_old_cache_objects_worker_thread' will get deleted when this loop exits.
        # Other calls of '_delete_old_cache_objects_in_separate_thread' would create a new thread if the reference is None.
        # To prevent spawning dozens of short-lived threads, this thread is kept alive a little longer than necessary.
        # (*sleep_1) DELETE_THREAD_SLEEP_1:
        #     One short sleep is within the loop. The sleep is skipped if there are too many slots still to be deleted.
        # (*sleep_2) DELETE_THREAD_SLEEP_2:
        #     A long sleep keeps the thread awake just before it would stop and checks again if there are entries
        #     to be deleted. This trades off keeping a thread alive with a longer time vs. spawning many new threads
        #     when there are lots of cache entries added in a burst.
        while True:
            # release the lock after every access such that this thread does not block
            # access to the cache for long
            occupied_slots = 0
            with self._cache_lock:
                occupied_slots = len(self)

            if occupied_slots <= self.slots:
                time.sleep(self.DELETE_THREAD_SLEEP_2)  # (*sleep_2)
                with self._cache_lock:
                    occupied_slots = len(self)

            if occupied_slots <= self.slots:
                # No cache items have been added during (*sleep_2)
                # -> Thread can terminate. A new thread will potentially get spawned with the next cache access.
                break

            with self._cache_lock:
                delete_candidates = []
                for owner, owner_cache in self._cache.items():
                    if len(owner_cache) == 0:
                        continue
                    for cache_function, owner_function_cache in owner_cache.items():
                        if len(owner_function_cache) == 0:
                            continue
                        least_recently_used_key, cache_obj = min(owner_function_cache.items(), key=lambda item: item[1].last_access)
                        delete_candidates.append(((owner, cache_function, least_recently_used_key), cache_obj))
                (delete_owner, delete_cache_function, delete_key), _ = min(delete_candidates, key=lambda item: item[1].last_access)
                del self._cache[delete_owner][delete_cache_function][delete_key]
                if len(self._cache[delete_owner][delete_cache_function]) == 0:
                    del self._cache[delete_owner][delete_cache_function]
                    if len(self._cache[delete_owner]) == 0:
                        del self._cache[delete_owner]

                if len(self) > (self.slots + 10):
                    # Skip (*sleep_1) as there is a lot work still to do.
                    continue

            time.sleep(self.DELETE_THREAD_SLEEP_1)  # (*sleep_1)
        # remove reference such that a new thread can be started
        with self._delete_old_cache_objects_worker_thread_lock:
            self._delete_old_cache_objects_worker_thread = None

    def _delete_old_cache_objects_in_separate_thread(self):
        with self._cache_lock:
            if len(self) <= self.slots:
                return
        with self._delete_old_cache_objects_worker_thread_lock:
            if self._delete_old_cache_objects_worker_thread is not None:
                return
            self._delete_old_cache_objects_worker_thread = threading.Thread(target=self._delete_old_cache_objects_loop)
        self._delete_old_cache_objects_worker_thread.start()

    def delete(self, cache_owner):
        with self._cache_lock:
            if cache_owner not in self._cache:
                return
            del self._cache[cache_owner]


class AsyncSharedCache:
    DEFAULT_THREADPOOL_WORKERS = multiprocessing.pool.ThreadPool(multiprocessing.cpu_count() - 1)
    DEFAULT_THREADPOOL_WAITERS = multiprocessing.pool.ThreadPool(10)
    slots = RWDescriptor()

    def __init__(self, slots, worker_pool=None, waiter_pool=None):
        self._cache = SizeRestrictedCache(slots)
        self.worker_pool = worker_pool if worker_pool is not None else AsyncSharedCache.DEFAULT_THREADPOOL_WORKERS
        self.waiter_pool = waiter_pool if waiter_pool is not None else AsyncSharedCache.DEFAULT_THREADPOOL_WAITERS

    def get_slots(self):
        return self._cache.slots

    def set_slots(self, value):
        self._cache.slots = value

    def get_cache_state(self, async_shared_cache_query_policy, *args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        return self._cache.get_cache_state(
            async_shared_cache_query_policy.query_owner,
            async_shared_cache_query_policy.function,
            key,
        )

    def query(self, async_shared_cache_query_policy, *args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        cache_object = self._cache.query_cache_object(
            async_shared_cache_query_policy.query_owner,
            async_shared_cache_query_policy.function,
            key,
        )

        cache_hit = cache_object.touched # cache already has an entry for this query, the entry might be ready or not at this point
        cache_object.touch() # touch as early as possible such that other calls will not try to execute the actual query too
        # data is already in cache and ready to be returned
        # -> asynchroneously execute callback, return data
        if cache_object.is_ready():
            if async_shared_cache_query_policy.callback is not None:
                # still execute the callback function as requested
                AsyncExecutePolicy(async_shared_cache_query_policy.callback)(self.worker_pool, cache_object.data)
            return cache_object.data
        # data is not already in cache
        # no placeholder can be returned
        # -> valid data must be returned immediately: synchroneously fetch data and put data into cache, asynchroneously execute callback, return data
        elif async_shared_cache_query_policy.result_placeholder == AsyncSharedCacheQueryPolicy.NONE:
            if not cache_hit:
                cache_object.set_data(async_shared_cache_query_policy.function(*args, **kwargs))
            cache_object.wait()
            if async_shared_cache_query_policy.callback is not None:
                AsyncExecutePolicy(async_shared_cache_query_policy.callback)(self.waiter_pool, cache_object.data)
            return cache_object.data
        # data is not already in cache
        # placeholder can be returned
        # -> cache entry is freshly created and must be filled with data: asynchroneously fetch data, put data into cache and execute callback, return placeholder
        elif not cache_hit: # cache is missing data
            def callback_wrapper(result):
                cache_object.set_data(result)
                if async_shared_cache_query_policy.callback is not None:
                    async_shared_cache_query_policy.callback(result)
            AsyncExecutePolicy(
                async_shared_cache_query_policy.function,
                callback_wrapper,
            )(self.worker_pool, *args, **kwargs)
            return async_shared_cache_query_policy.result_placeholder
        # data is not already in cache
        # placeholder can be returned
        # cache entry is not fresh
        # -> fetching of data is already in progress: asynchroneously wait for data and execute callback, return placeholder
        else:
            if async_shared_cache_query_policy.callback is not None:
                def wait_for_cache_data():
                    cache_object.wait()
                    return cache_object.data
                AsyncExecutePolicy(
                    wait_for_cache_data,
                    async_shared_cache_query_policy.callback,
                )(self.waiter_pool)
            return async_shared_cache_query_policy.result_placeholder

    def delete_cache(self, cache_owner):
        self._cache.delete(cache_owner)
