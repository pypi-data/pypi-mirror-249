# SPDX-FileCopyrightText: 2023 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-2.0-only

import datetime
import itertools
import logging
import json
import os
import threading
import uuid


# serizalized MetaStorageObject:
# {
#   'update_timestamp': '2023-10-20T15:00:00.000000+00:00' 
#   'filename': '<filename>'
#   'meta': {
#     'key_1': 'abc',
#     'key_2': 2
#   }
# }
class MetaStorageObject:
    VERSION = "1.0"
    def __init__(self, filename, meta=None, update_timestamp=None):
        self._filename = filename
        self._meta = dict() if meta is None else meta
        update_timestamp = datetime.datetime.now(datetime.timezone.utc) if update_timestamp is None else update_timestamp
        self._set_update_timestamp(update_timestamp)

    @staticmethod
    def load_serialized(serialized_data):
        try:
            assert "filename" in serialized_data, "'filename' missing in meta data, data invalid"
            assert "meta" in serialized_data, "'meta' missing in meta data, data invalid"
            assert "update_timestamp" in serialized_data, "'update_timestamp' missing in meta data, data invalid"
            assert serialized_data.get("version", "1.0") == "1.0", f"version {serialized_data.get('version', '1.0')} not supported"
        except AssertionError as e:
            raise MetaStorage.LoadException(f"Error loading meta data '{serialized_data}'", e)
        filename = serialized_data["filename"]
        meta = serialized_data["meta"]
        update_timestamp = datetime.datetime.fromtimestamp((serialized_data["update_timestamp"] / 1000), tz=datetime.timezone.utc)
        return MetaStorageObject(filename, meta, update_timestamp)

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, new_filename):
        if new_filename != self._filename:
            self._filename = new_filename
            self._touch()

    @property
    def meta(self):
        return self._meta

    @meta.setter
    def meta(self, new_meta):
        if new_meta == self._meta:
            return
        self._meta = new_meta
        self._touch()

    @property
    def update_timestamp(self):
        return self._update_timestamp

    def _set_update_timestamp(self, new_timestamp):
        assert isinstance(new_timestamp, datetime.datetime)
        assert new_timestamp.tzinfo == datetime.timezone.utc
        self._update_timestamp = new_timestamp.replace(
            microsecond=(new_timestamp.microsecond - (new_timestamp.microsecond % 1000)),
        )

    def _touch(self):
        self._set_update_timestamp(datetime.datetime.now(datetime.timezone.utc))

    def update_meta(self, meta):
        self.meta.update(meta)
        self._touch()

    def delete_meta(self, meta_path):
        MetaStorageObject._recursive_delete_meta_path(self.meta, list(meta_path))
        self._touch()

    @staticmethod
    def _recursive_delete_meta_path(subdict, delete_path):
        if len(delete_path) == 0:
            return True
        delete_key = delete_path.pop(0)
        if delete_key in subdict:
            do_delete = MetaStorageObject._recursive_delete_meta_path(subdict[delete_key], delete_path)
            if do_delete:
                del subdict[delete_key]
                if len(subdict) == 0:
                    return True
        return False

    def serialize(self):
        out = dict(
            filename=self._filename,
            update_timestamp=int(self._update_timestamp.timestamp() * 1000),
            meta=self._meta,
        )
        if self.VERSION != "1.0":
            out.update({"version": self.VERSION})
        return out


class MetaStorageVersionUtil:
    @staticmethod
    def left_version_less_equal(left, right):
        return [int(v) for v in left.split(".")] <= [int(v) for v in right.split(".")]


# serizalized MetaStorage:
# {
#   'data': {
#     '<hash>' : '<MetaStorageObject_serialized>'
#   }
# }
class MetaStorage:
    VERSION="1.0"
    _instances = dict()
    _instances_lock = threading.Lock()

    _meta_extension = ".meta"

    class LoadException(Exception):
        def __init__(self, message, exceptions=[]):
            self.message = message
            if not isinstance(exceptions, (tuple, list)):
                exceptions = [exceptions]
            self.exceptions = exceptions

        def __str__(self):
            linesep = f"{os.linesep}  "
            return f"{self.message}:{linesep}" + linesep.join(itertools.chain(*(str(e).splitlines() for e in self.exceptions)))

    @staticmethod
    def get_abs_directory(path):
        try:
            assert os.path.exists(path), f"{path} does not exist"
        except AssertionError as e:
            raise MetaStorage.LoadException(f"Could not load meta storage for '{path}'", e)

        if os.path.isfile(path):
            path = os.path.dirname(path)
        return os.path.abspath(path)

    def __new__(cls, path):
        abs_directory = MetaStorage.get_abs_directory(path)
        with cls._instances_lock:
            if abs_directory in cls._instances:
                return cls._instances[abs_directory]

            instance = super().__new__(cls)
            instance._initialized = False
            cls._instances[abs_directory] = instance
        return instance

    def __init__(self, path):
        if self._initialized == True: return

        self._initialized = True

        self.path = MetaStorage.get_abs_directory(path)
        self._meta_path = None
        self._data = dict()

        self.load_exception = None
        self._load_meta_data()

    def __len__(self):
        return len(self._data)

    def get_hashes(self):
        return list(self._data.keys())

    def _load_meta_data(self):
        meta_files = self._find_meta_files()

        meta_files_fully_loaded = list()
        meta_file_load_exceptions = list()
        self._data = dict()
        for meta_file in meta_files:
            exception_ocurred = False
            try:
                meta_storage_data = self._load_meta_file(meta_file)
            except Exception as e:
                exception_ocurred = True
                meta_file_load_exceptions.append(
                    MetaStorage.LoadException(f"Could not process file '{meta_file}' for meta data", e)
                )
                continue

            for hash, meta_storage_data_object_data in meta_storage_data["data"].items():
                try:
                    meta_storage_object = MetaStorageObject.load_serialized(meta_storage_data_object_data)
                    if hash in self._data and self._data[hash].update_timestamp > meta_storage_object.update_timestamp:
                        continue
                    self._data[hash] = meta_storage_object
                except Exception as e:
                    meta_file_load_exceptions.append(
                        MetaStorage.LoadException(f"Could not fully process file '{meta_file}' for meta data", e)
                    )
                    exception_ocurred = True
                    continue
            if not exception_ocurred:
                meta_files_fully_loaded.append(meta_file)

        self._meta_path = None
        if len(meta_files) == 1:
            self._meta_path = meta_files[0]
        self._store_data()
        for meta_file in (f for f in meta_files_fully_loaded if f != self._meta_path):
            os.remove(meta_file)


        if len(meta_file_load_exceptions) > 0:
            # raise Exception to safely use logging.Logger.exception
            # According to Python docs (version 3.12.1) for 'logging.Logger.exception':
            # "This method should only be called from an exception handler"
            try:
                raise MetaStorage.LoadException(f"Errors occurred when loading meta storage for path '{self.path}'", meta_file_load_exceptions)
            except MetaStorage.LoadException as e:
                logging.getLogger(__name__).exception(f"Exception occurred when loading meta data")
                self.load_exception = e

    def _find_meta_files(self):
        abs_paths = (os.path.abspath(os.path.join(self.path, file_)) for file_ in os.listdir(self.path) if file_.endswith(self._meta_extension))
        return [path for path in abs_paths if os.path.isfile(path)]

    @staticmethod
    def _load_meta_file(path):
        with open(path, "r") as file_:
            meta_storage_data = json.loads(file_.read())
        try:
            assert "data" in meta_storage_data, "'data' missing in meta storage"
            version = meta_storage_data.get("version", "1.0")
            assert MetaStorageVersionUtil.left_version_less_equal(version, "1.0"), f"metastorage.version={version} not supported"
        except AssertionError as e:
            raise MetaStorage.LoadException(f"Meta file '{path}' corrupt", e)
        return meta_storage_data

    def _store_data(self):
        if len(self._data) == 0:
            if self._meta_path is not None and os.path.exists(self._meta_path):
                os.remove(self._meta_path)
            return

        if self._meta_path is None:
            self._meta_path = os.path.abspath(os.path.join(self.path, f"{uuid.uuid4().hex}{self._meta_extension}"))

        meta_storage_data = dict()
        for hash, meta_storage_object in self._data.items():
            meta_storage_data[hash] = meta_storage_object.serialize()
        
        meta_storage = dict(data=meta_storage_data)
        if self.VERSION != "1.0":
            meta_storage.update({"version": self.VERSION})

        with open(self._meta_path, "w") as file_:
            file_.write(json.dumps(meta_storage))

    def _get_meta_storage_object(self, hash, filename):
        do_store = False
        meta_storage_object = self._data.get(hash, None)
        if meta_storage_object is None:
            meta_storage_object = MetaStorageObject(filename)
            self._data[hash] = meta_storage_object
        if filename is not None and filename != meta_storage_object.filename:
            meta_storage_object.filename = filename
            do_store = True
        if do_store:
            self._store_data()
        return meta_storage_object

    def delete_meta_storage_object(self, hash):
        if hash in self._data:
            del self._data[hash]
        self._store_data()

    def set_meta(self, hash, filename, meta):
        meta_storage_object = self._get_meta_storage_object(hash, filename)
        if meta != meta_storage_object.meta:
            meta_storage_object.meta = meta
            self._store_data()

    def update_meta(self, hash, filename, meta):
        meta_storage_object = self._get_meta_storage_object(hash, filename)
        storage_meta = meta_storage_object.meta
        if any(storage_meta.get(k, object()) != v for k, v in meta.items()):
            meta_storage_object.update_meta(meta)
            self._store_data()

    def delete_meta(self, hash, filename, meta_path=None):
        assert meta_path is None or isinstance(meta_path, (list, tuple))
        meta_storage_object = self._get_meta_storage_object(hash, filename)
        if meta_path is None:
            meta_storage_object.meta = {}
        else:
            meta_storage_object.delete_meta(meta_path)
        self._store_data()

    def get_meta(self, hash, filename=None):
        return self._get_meta_storage_object(hash, filename).meta
