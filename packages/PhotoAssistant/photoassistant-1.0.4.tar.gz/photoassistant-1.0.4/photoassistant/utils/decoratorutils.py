# SPDX-FileCopyrightText: 2023 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-2.0-only

from photoassistant.utils.cachingutils import AsyncSharedCacheQueryPolicy

class async_cached_query:
    # A decorator that evaluates special keyword arguments and modifies the original function.
    # Enables utilizing AsyncSharedCache, but the cache can also be ignored entirely. Furthermore, the cache can also be inspected.
    # Special keyword arguments:
    # 'query_ignore_cache':       default=False - set to False if cache should be fully ignored
    # 'query_cache_state_only':   default=False - do not execute the query, only peek into cache if value is available
    # 'query_callback':           default=None - sets a callback to be called when the result is available
    # 'query_result_placeholder': default=AsyncSharedCacheQueryPolicy.NONE - value to be returned if the value is not yet cached

    def __init__(self, async_shared_cache):
        self.async_shared_cache = async_shared_cache

    def __call__(self, function):
        def decorated_function(self_, *args, query_ignore_cache=False, query_cache_state_only=False, query_callback=None, query_result_placeholder=AsyncSharedCacheQueryPolicy.NONE, **kwargs):
            if query_ignore_cache:
                return function(self_, *args, **kwargs)

            async_shared_cache_query_policy = AsyncSharedCacheQueryPolicy(
                self_, # self_ is 'self' of the instance calling the decorated method -> here it is also the owner of the query
                function,
                callback=query_callback,
            )
            async_shared_cache_query_policy.set_result_placeholder(query_result_placeholder)

            if query_cache_state_only:
                return self.async_shared_cache.get_cache_state(async_shared_cache_query_policy, self_, *args, **kwargs)
            return self.async_shared_cache.query(async_shared_cache_query_policy, self_, *args, **kwargs)
        return decorated_function
