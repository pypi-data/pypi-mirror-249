# SPDX-FileCopyrightText: 2023 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-2.0-only

import os
import re

from photoassistant.core.photo import PhotoAsyncSharedCached
from photoassistant.gui.qt.utils.qtutils import QPixmapLoader
from photoassistant.utils.cachingutils import AsyncSharedCache
from photoassistant.utils.decoratorutils import async_cached_query


class PhotoQt(PhotoAsyncSharedCached):
    ASYNC_SHARED_CACHE_IMAGES = AsyncSharedCache(slots=100)
    SUPPORTED_FILES_RE = re.compile(r"^.*((\.bmp)|(\.gif)|(\.jpe?g)|(\.png)|(\.pbm)|(\.pgm)|(\.ppm)|(\.xbm)|(\.xpm)|(\.svg))$")

    @staticmethod
    def file_is_supported(path):
        return PhotoQt.SUPPORTED_FILES_RE.match(path) is not None and os.path.exists(path)

    #override
    def set_orientation_correction(self, orientation_correction):
        super().set_orientation_correction(orientation_correction)
        self.ASYNC_SHARED_CACHE_IMAGES.delete_cache(self)

    #override
    @async_cached_query(ASYNC_SHARED_CACHE_IMAGES)
    def get_image(self, max_size=None, **kwargs):
        # Special keyword arguments:
        # 'query_ignore_cache':       default=False - set to False if cache should be fully ignored
        # 'query_cache_state_only':   default=False - do not execute the query, only peek into cache if value is available
        # 'query_callback':           default=None - sets a callback to be called when the result is available
        # 'query_result_placeholder': default=AsyncSharedCacheQueryPolicy.NONE - value to be returned if the value is not yet cached
        orientation_correction = self.get_orientation_correction()
        return QPixmapLoader.load(
            self.get_path(),
            max_size=max_size,
            orientation_correction=orientation_correction,
        )
