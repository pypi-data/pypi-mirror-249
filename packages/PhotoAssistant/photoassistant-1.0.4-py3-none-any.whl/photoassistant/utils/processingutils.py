# SPDX-FileCopyrightText: 2023 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-2.0-only

class AsyncExecutePolicy:
    def __init__(self, function, callback=None):
        self.function = function
        self.callback = callback

    def __call__(self, worker_pool, *args, **kwargs):
        worker_pool.apply_async(
            self.function,
            args,
            kwargs,
            callback=self.callback
        )
