# SPDX-FileCopyrightText: 2023 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-2.0-only

import os
import itertools


class FileSystemScanner:
    @staticmethod
    def find_supported_files(paths, filter_function=lambda _: True):
        def _find_photo_object_files(path):
            photo_object_paths = list()
            if path is None:
                return photo_object_paths
            for root, _, files in os.walk(path):
                root_path = os.path.abspath(root)
                for file in files:
                    abs_path = os.path.join(root_path, file)
                    if filter_function(abs_path) is True:
                        photo_object_paths.append(abs_path)
            return photo_object_paths
        if not isinstance(paths, (list, tuple)):
            paths = (paths,)
        return list(sorted(itertools.chain.from_iterable(_find_photo_object_files(p) for p in paths)))
