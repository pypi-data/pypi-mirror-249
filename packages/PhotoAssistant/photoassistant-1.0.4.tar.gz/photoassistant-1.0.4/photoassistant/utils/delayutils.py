# SPDX-FileCopyrightText: 2023 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-2.0-only

import threading
import time


class DelayedQueryManager:
    # This class basically allows to schedule computational intensive
    # tasks delayed such that they can still be cancelled within a short
    # time frame. This functionality is useful e.g., for a
    # PhotoViewer implementation where scrolling from top to bottom
    # calls a function that queries all images the way from top to
    # bottom. The DelayedQueryManger helps by delaying every query just
    # a very little bit such that it is not too late to cancel the actual
    # computationally intensive task before it starts. This way a lot
    # of scrolling would result in the creation of many delayed tasks
    # most of which get cancelled before they actually consume
    # CPU resources.
    QUERY_DELAY = 0.1 # in s delay before a query is really executed
    def __init__(self):
        self.pending_queries = list()
        self.pending_queries_lock = threading.Lock()
        self.max_queries = None

    def set_max_queries(self, value):
        self.max_queries = value

    class DelayedQuery:
        def __init__(self, query):
            self.query = query
            self.timer_thread = None
            self.stop_event = threading.Event()

        def start(self):
            def wrapped():
                time.sleep(DelayedQueryManager.QUERY_DELAY)
                if self.stop_event.is_set():
                    return
                self.query()
            self.timer_thread = threading.Thread(target=wrapped)
            self.timer_thread.start()

        def stop(self):
            if self.timer_thread is not None:
                self.stop_event.set()
            self.timer_thread = None

    def start_query_if_none_pending(self, query_key, query):
        with self.pending_queries_lock:
            matching_pending_queries = [elem for elem in self.pending_queries if elem[0] == query_key]
            if len(matching_pending_queries) == 0:
                if self.max_queries is not None:
                    while len(self.pending_queries) > self.max_queries:
                        _, delayed_query = self.pending_queries.pop(0)
                        delayed_query.stop()
                    delayed_query = self.DelayedQuery(query)
                    self.pending_queries.append((query_key, delayed_query))
                    delayed_query.start()
            else:
                # reprioritize existing queries by moving them to the end of the list
                # such that they do not get deleted next
                for matching_pending_query in matching_pending_queries:
                    self.pending_queries.remove(matching_pending_query)
                    self.pending_queries.append(matching_pending_query)

    def stop_query_if_pending(self, query_key):
        with self.pending_queries_lock:
            for matching_pending_query in (elem for elem in self.pending_queries if elem[0] == query_key):
                self.pending_queries.remove(matching_pending_query)
                _, query = matching_pending_query
                query.stop()
