# SPDX-FileCopyrightText: 2023 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-2.0-only

import datetime
import exifread
import hashlib
import logging
import mmap
import os
import re

from photoassistant.core.metastorage import MetaStorage
from photoassistant.utils.cachingutils import AsyncSharedCache
from photoassistant.utils.descriptors import RDescriptor
from photoassistant.utils.descriptors import RWDescriptor
from photoassistant.utils.decoratorutils import async_cached_query

# exifread prints a warning 'PNG file does not have exif data.' when exif data
# is not present. This workaround is to get rid of the warning.
logging.getLogger("exifread").setLevel(logging.ERROR)

class PhotoHash:
    @staticmethod
    def sha256(path):
        hash_object = hashlib.sha256()
        with open(path, "rb") as file_:
            with mmap.mmap(file_.fileno(), 0, access=mmap.ACCESS_READ) as map:
                hash_object.update(map)
        return hash_object.hexdigest()


class PhotoInterface:
    path = RWDescriptor()
    filename = RDescriptor()
    main_tag = RWDescriptor()
    tags = RDescriptor()
    all_tags = RDescriptor()
    creation_timestamp = RWDescriptor()
    orientation_correction = RWDescriptor()
    gps_coordinates = RWDescriptor()
    hash = RDescriptor()
    image = RDescriptor()

    def __init__(self, path):
        path = os.path.abspath(path)
        assert self.file_is_supported(path)
        self._path = path

    def get_path(self):
        return self._path

    def get_filename(self):
        return os.path.basename(self._path)

    def add_tag(self, tag):
        raise NotImplementedError()

    def delete_tag(self, tag):
        raise NotImplementedError()

    @staticmethod
    def file_is_supported(file):
        raise NotImplementedError()


class Photo(PhotoInterface):
    meta = RDescriptor()
    exif = RDescriptor()

    class TagFormatException(Exception):
        pass

    TAG_ALLOWED_CHARACTERS = r"[a-zA-Z0-9_+\-*/#'!%~\(\)&?\.,;]"
    MAIN_TAG_REGEX = re.compile(r"(?:\:" + TAG_ALLOWED_CHARACTERS + "+)+")
    TAG_REGEX = re.compile("^" + TAG_ALLOWED_CHARACTERS + "+$")
    # mapping of exif id to correction matrices for images centered in the origin
    EXIF_ORIENTATION_CORRECTION_MATRIX_MAP = {
        1: [1, 0, 0, 0, 1, 0, 0, 0, 1],
        2: [-1, 0, 0, 0, 1, 0, 0, 0, 1],
        3: [-1, 0, 0, 0, -1, 0, 0, 0, 1],
        4: [1, 0, 0, 0, -1, 0, 0, 0, 1],
        5: [0, 1, 0, 1, 0, 0, 0, 0, 1],
        6: [0, 1, 0, -1, 0, 0, 0, 0, 1],
        7: [0, -1, 0, -1, 0, 0, 0, 0, 1],
        8: [0, -1, 0, 1, 0, 0, 0, 0, 1],
    }

    def get_exif(self):
        with open(self.get_path(), "rb") as file_:
            with mmap.mmap(file_.fileno(), 0, access=mmap.ACCESS_READ) as mmap_:
                try:
                    return exifread.process_file(mmap_, details=False)
                except Exception:
                    logging.getLogger(__name__).exception(f"Processing file '{self.get_path()}' for exif data failed")
                    return dict()

    def get_meta(self):
        return MetaStorage(self.get_path()).get_meta(self.get_hash(), self.get_filename())

    def get_all_tags(self):
        return list(self.get_meta().get("tags", []))

    def get_tags(self):
        return [t for t in self.get_all_tags() if not t.startswith(":")]

    def get_main_tag(self):
        for tag in filter(lambda t: t.startswith(":"), self.get_all_tags()):
            return tag  # return first tag if present
        return None

    def set_main_tag(self, tag):
        if self.get_main_tag() != tag:
            all_tags = self.get_tags()
            if tag is not None:
                try:
                    assert self.MAIN_TAG_REGEX.match(tag)
                except AssertionError:
                    raise Photo.TagFormatException(f"Tag '{tag}' is ill-formatted")
                all_tags = [tag] + all_tags
            MetaStorage(self.get_path()).update_meta(self.get_hash(), self.get_filename(), meta={"tags": all_tags})

    def add_tag(self, tag):
        try:
            assert self.TAG_REGEX.match(tag)
        except AssertionError:
            raise Photo.TagFormatException(f"Tag '{tag}' is ill-formatted")
        if tag not in self.get_tags():
            all_tags = self.get_all_tags() + [tag]
            MetaStorage(self.get_path()).update_meta(self.get_hash(), self.get_filename(), meta={"tags": all_tags})

    def delete_tag(self, tag):
        if tag in self.get_tags():
            all_tags = self.get_all_tags()
            all_tags.remove(tag)
            MetaStorage(self.get_path()).update_meta(self.get_hash(), self.get_filename(), meta={"tags": all_tags})

    def get_creation_timestamp(self):
        meta_timestamp = self.get_meta().get("creation_timestamp")
        if meta_timestamp is not None:
            return datetime.datetime.fromtimestamp(meta_timestamp / 1000)

        exif_timestamp = self.get_exif().get("Image DateTime")
        if exif_timestamp is not None:
            return datetime.datetime.strptime(exif_timestamp.values, "%Y:%m:%d %H:%M:%S")

        return None

    def set_creation_timestamp(self, dt):
        assert isinstance(dt, datetime.datetime)
        assert dt.tzinfo is None
        MetaStorage(self.get_path()).update_meta(self.get_hash(), self.get_filename(), meta={"creation_timestamp": int(dt.timestamp() * 1000)})

    def _get_exif_orientation_correction(self):
        exif_orientation = self.get_exif().get("Image Orientation")
        if exif_orientation is not None:
            exif_orientation = exif_orientation.values[0]
            # Even though only values 1 to 8 are valid exif orientation meta data values,
            # some cameras use e.g., 0 for panorama images. Hence, we gracefully assume
            # 'no orientation' when the value is not between [1, 8].
            if 1 <= exif_orientation <= 8:
                return Photo.EXIF_ORIENTATION_CORRECTION_MATRIX_MAP[exif_orientation]
        return [1, 0, 0, 0, 1, 0, 0, 0, 1]

    def get_orientation_correction(self):
        meta_orientation = self.get_meta().get("orientation_correction")
        if meta_orientation is not None:
            return meta_orientation

        return self._get_exif_orientation_correction()

    def set_orientation_correction(self, orientation_correction):
        if (
            not isinstance(orientation_correction, (tuple, list))
            or len(orientation_correction) != 9
        ):
            raise ValueError("orientation_correction must be a list of 9 entries representing the values of a a 3x3 matrix")
        exif_orientation_correction = self._get_exif_orientation_correction()
        if exif_orientation_correction is not None and all(a == b for a, b in zip(orientation_correction, exif_orientation_correction)):
            MetaStorage(self.get_path()).delete_meta(self.get_hash(), self.get_filename(), ["orientation_correction"])
        else:
            MetaStorage(self.get_path()).update_meta(self.get_hash(), self.get_filename(), meta={"orientation_correction": orientation_correction})

    def _get_exif_gps_coordinates(self):
        def _get_exif_degrees_generic(orientation):
            coordinate = self.get_exif().get(f"GPS GPS{orientation}")
            coordinate_ref = self.get_exif().get(f"GPS GPS{orientation}Ref")
            if coordinate is None or coordinate_ref is None:
                return None
            d, m, s = coordinate.values
            try:
                coordinate_degrees = d + (m / 60) + (s / 3600)
                if coordinate_ref.values in ("S", "W"):
                    coordinate_degrees *= -1
            except ZeroDivisionError:
                return None
            return float(coordinate_degrees)

        def _get_altitude():
            value = self.get_exif().get(f"GPS GPSAltitude")
            value_ref = self.get_exif().get(f"GPS GPSAltitudeRef")
            if value is None or value_ref is None:
                return None
            value = value.values[0]
            if value_ref.values == 1:
                value *= -1
            return float(value)

        latitude = _get_exif_degrees_generic("Latitude")
        longitude = _get_exif_degrees_generic("Longitude")
        altitude = _get_altitude()
        meta_gps_coordinates = [latitude, longitude, altitude]
        return meta_gps_coordinates

    def get_gps_coordinates(self):
        meta_gps_coordinates = self.get_meta().get("gps_coordinates")
        if meta_gps_coordinates is not None:
            return meta_gps_coordinates
        return self._get_exif_gps_coordinates()

    def set_gps_coordinates(self, gps_coordinates):
        if (
            not isinstance(gps_coordinates, (tuple, list))
            or len(gps_coordinates) != 3
        ):
            raise ValueError("gps_coordinates must be a list of 3 entries representing latitude, longitude and altitude")
        exif_gps_coordinates = self._get_exif_gps_coordinates()
        if exif_gps_coordinates is not None and all(a == b for a, b in zip(gps_coordinates, exif_gps_coordinates)):
            MetaStorage(self.get_path()).delete_meta(self.get_hash(), self.get_filename(), ["gps_coordinates"])
        else:
            MetaStorage(self.get_path()).update_meta(self.get_hash(), self.get_filename(), meta={"gps_coordinates": gps_coordinates})

    def get_hash(self):
        return PhotoHash.sha256(self.get_path())


class PhotoAsyncSharedCached(Photo):
    ASYNC_SHARED_CACHE_EXIF = AsyncSharedCache(slots=100000)
    ASYNC_SHARED_CACHE_HASH = AsyncSharedCache(slots=100000)

    #override
    @async_cached_query(ASYNC_SHARED_CACHE_EXIF)
    def get_exif(self, **kwargs):
        # Special keyword arguments:
        # 'query_ignore_cache':       default=False - set to False if cache should be fully ignored
        # 'query_cache_state_only':   default=False - do not execute the query, only peek into cache if value is available
        # 'query_callback':           default=None - sets a callback to be called when the result is available
        # 'query_result_placeholder': default=AsyncSharedCacheQueryPolicy.NONE - value to be returned if the value is not yet cached
        return super().get_exif()

    #override
    @async_cached_query(ASYNC_SHARED_CACHE_HASH)
    def get_hash(self, **kwargs):
        # Special keyword arguments:
        # 'query_ignore_cache':       default=False - set to False if cache should be fully ignored
        # 'query_cache_state_only':   default=False - do not execute the query, only peek into cache if value is available
        # 'query_callback':           default=None - sets a callback to be called when the result is available
        # 'query_result_placeholder': default=AsyncSharedCacheQueryPolicy.NONE - value to be returned if the value is not yet cached
        return super().get_hash()
