# SPDX-FileCopyrightText: 2023 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-2.0-only

import logging
import datetime
import os
import re
import shutil

from photoassistant.core.filescan import FileSystemScanner
from photoassistant.core.metastorage import MetaStorage
from photoassistant.utils.descriptors import SettingsDescriptor

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


class PhotoIndex:
    def __init__(self, photo_delegate):
        self.root_path = None
        self._photos = []
        self._photo_delegate = photo_delegate

    def load(self, path, sort_key=None):
        self.root_path = path
        self._photos = self.load_photos()
        if sort_key is not None:
            self.sort(sort_key)

    def copy(self):
        photo_index = PhotoIndex(self._photo_delegate)
        photo_index.root_path = self.root_path
        photo_index._photos = self._photos.copy()
        return photo_index

    def sort(self, key):
        self._photos.sort(key=key)

    def __getitem__(self, index):
        return self._photos[index]

    def __len__(self):
        return len(self._photos)

    def __iter__(self):
        return (p for p in self._photos)

    def index(self, photo):
        return self._photos.index(photo)

    def load_photos(self):
        photo_paths = FileSystemScanner.find_supported_files(self.root_path, filter_function=self._photo_delegate.file_is_supported)
        return [self._photo_delegate(path) for path in photo_paths]

    def remove(self, photo):
        self._photos.remove(photo)


class PhotoCollectionSettings:
    FILENAME = "collection.config"

    # SettingsDescriptor descriptors automatically create, populate and update
    # a variable '_settings' which keeps all descriptor attributes in a dictionary
    # with serialized values
    _settings = dict() # initialized here just to make clear that this variable exists
    tagged_photos_root_folder = SettingsDescriptor("", lambda value: re.search(r"(\w*)", value).group(1))  # SettingsDescriptor will catch if re.search returns None
    deleted_photos_folder = SettingsDescriptor("deleted", lambda value: re.search(r"(\w*)", value).group(1))  # SettingsDescriptor will catch if re.search returns None

    def __init__(self, version, path):
        assert os.path.exists(path) and os.path.isdir(path)
        self.path = os.path.join(os.path.abspath(path), PhotoCollectionSettings.FILENAME)
        self.version = version

    @classmethod
    def load(cls, path):
        settings_path = os.path.join(path, PhotoCollectionSettings.FILENAME)
        settings = None
        # match something in the form 'key=value' or 'key=" value with spaces "'
        key_value_pair_re = re.compile(r"^\s*(\S+)\s*=\s*((?:\".*\")|(?:\S+))\s*$")
        with open(settings_path, "r") as file_:
            first_line = file_.readline()
            version_match = key_value_pair_re.match(first_line)
            assert version_match is not None
            key, version = version_match.groups()
            version = version.strip("\"")
            assert key == "version"
            assert version == "1.0"
            settings = cls(version, path)

            for line in file_.readlines():
                line_match = key_value_pair_re.match(line)
                if line_match is None:
                    continue
                key, value = line_match.groups()
                value = value.strip("\"")
                if hasattr(settings, key):
                    setattr(settings, key, value)
                else:
                    logger.warning(f"Setting {key}='{value}' is discarded by {cls.__name__}")
        settings.assert_settings()
        return settings

    def store(self):
        self.assert_settings()
        any_whitespace_match_re = re.compile(r"^.*\s.*$")
        with open(self.path, "w") as file_:
            file_.write(f"version={self.version}")
            for key in sorted(self._settings.keys()):
                file_.write(os.linesep)
                value = self._settings[key]
                if any_whitespace_match_re.match(value) or len(value) == 0:
                    value = f"\"{value}\""
                file_.write(f"{key} = {value}")

    def assert_settings(self):
        assert self.tagged_photos_root_folder != self.deleted_photos_folder

    @staticmethod
    def _find_settings_files(path):
        path_abs = os.path.abspath(os.path.normpath(path))
        assert os.path.isdir(path_abs)

        # This function searches for PhotoCollectionSettings.
        # The search starts from the directory closest to root and looks into every directory
        # in the path. If no settings are found 'above' the path (in the parent directories),
        # search continues into the children directories in the order os.walk traverses the
        # filesystem.
        settings_files = list()

        # search in parent directories
        search_paths = [path_abs]
        while True:
            path_part, folder = os.path.split(search_paths[0])
            if folder == "":
                break
            # the path closer to root gets inserted to the beginning of the list
            search_paths.insert(0, path_part)

        for p in search_paths:
            collection_settings_path = os.path.join(p, PhotoCollectionSettings.FILENAME)
            if os.path.exists(collection_settings_path):
                settings_files.append(collection_settings_path)

        # search in child directories
        for root, _, _ in os.walk(path):
            if root == search_paths[-1]:
                # avoid duplicate search results in the 'path' itself
                continue
            collection_settings_path = os.path.join(root, PhotoCollectionSettings.FILENAME)
            if os.path.exists(collection_settings_path):
                settings_files.append(collection_settings_path)
        return settings_files


class PhotoCollectionMetaStorageManager:
    def __init__(self, collection_root):
        self.collection_root = collection_root
        self.collection_root_meta_storage = MetaStorage(self.collection_root)

    @staticmethod
    def _recursive_delete_empty_directories(path):
        path = os.path.abspath(path)
        assert os.path.isdir(path)
        if len(os.listdir(path)) == 0:
            parent_path = os.path.dirname(path)
            os.rmdir(path)
            PhotoCollectionMetaStorageManager._recursive_delete_empty_directories(parent_path)

    @staticmethod
    def migrate_meta_data(hash, old_meta_path, new_meta_path):
        if new_meta_path == old_meta_path:
            return

        old_photo_meta_storage = MetaStorage(old_meta_path)
        if hash not in old_photo_meta_storage._data:
            return

        new_photo_meta_storage = MetaStorage(new_meta_path)
        if hash not in new_photo_meta_storage._data or old_photo_meta_storage._data[hash].update_timestamp > new_photo_meta_storage._data[hash].update_timestamp:
            filename = old_photo_meta_storage._data[hash].filename
            meta = old_photo_meta_storage._data[hash].meta
            new_photo_meta_storage.set_meta(hash, filename, meta=meta)
        old_photo_meta_storage.delete_meta_storage_object(hash)

    def find_all_directories_with_meta_files(self, root_path=None):
        if root_path is None:
            root_path = self.collection_root
        assert os.path.exists(root_path)
        return [root for root, _, files in os.walk(root_path) if any(f.endswith(MetaStorage._meta_extension) for f in files)]

    def _cleanup_meta_data_and_directories(self, photo_index):
        meta_directories = self.find_all_directories_with_meta_files(photo_index.root_path)
        for meta_directory in meta_directories:
            meta_storage = MetaStorage(meta_directory)
            meta_storage_hashes = set(meta_storage._data.keys())
            photo_hashes_present = set(photo.get_hash() for photo in photo_index if os.path.dirname(photo.get_path()) == meta_directory)
            orphaned_meta_storage_hashes = meta_storage_hashes.difference(photo_hashes_present)
            for hash in orphaned_meta_storage_hashes:
                self.migrate_meta_data(hash, meta_directory, self.collection_root)
            self._recursive_delete_empty_directories(meta_directory)

    def _migrate_collection_root_meta_data(self, photo_index):
        for photo in photo_index:
            hash = photo.get_hash()
            if hash in self.collection_root_meta_storage._data:
                self.migrate_meta_data(hash, self.collection_root, os.path.dirname(photo.get_path()))

    def cleanup_and_migrate_meta_data_and_directories(self, photo_index):
        self._cleanup_meta_data_and_directories(photo_index)
        self._migrate_collection_root_meta_data(photo_index)


class PhotoCollectionManager:
    VERSION = "1.0"

    class CollectionError(Exception):
        pass

    def __init__(self, photo_delegate):
        self.photo_delegate = self.hook_and_connect_photo_delegate(photo_delegate)
        self.photo_index = PhotoIndex(self.photo_delegate)
        self.collection_root = None
        self.meta_storage_manager = None

    def set_collection_root(self, path):
        path_abs = os.path.abspath(path)
        collection_root = self.find_collection(path_abs)
        assert collection_root is not None
        self.collection_root = collection_root
        self.collection_settings = PhotoCollectionSettings.load(self.collection_root)
        self.meta_storage_manager = PhotoCollectionMetaStorageManager(self.collection_root)

    @staticmethod
    def create(path):
        path_abs = os.path.abspath(path)
        assert PhotoCollectionManager.find_collection(path_abs) is None
        collection_settings = PhotoCollectionSettings(PhotoCollectionManager.VERSION, path_abs)
        collection_settings.store()

    @staticmethod
    def find_collection(path):
        path_abs = os.path.abspath(path)
        settings_paths = PhotoCollectionSettings._find_settings_files(path_abs)
        if len(settings_paths) > 1:
            raise PhotoCollectionManager.CollectionError(
                f"Multiple collection settings found: {settings_paths}.",
            )
        if len(settings_paths) == 0:
            return None
        collection_root = os.path.dirname(settings_paths[0])
        return collection_root

    def open_photos(self, path, sort_key=None):
        path_abs = os.path.abspath(path)
        assert os.path.isdir(path_abs)
        self.photo_index.load(path_abs, sort_key) 

    def delete_photo(self, photo):
        assert self.collection_root is not None
        deleted_photos_folder = self.collection_settings.deleted_photos_folder
        assert isinstance(deleted_photos_folder, str)
        if deleted_photos_folder is None or deleted_photos_folder == "":
            os.remove(photo.get_path())
        else:
            deleted_photo_path = os.path.join(
                self.collection_root,
                deleted_photos_folder,
                photo.get_filename(),
            )
            photo.set_path(deleted_photo_path)
        if photo in self.photo_index:
            self.photo_index.remove(photo)

    @staticmethod
    def delete_duplicate_photos(photo_index):
        photo_index_root_path = photo_index.root_path
        photo_index_photo_delegate = photo_index._photo_delegate
        all_photo_hashes = set(photo.get_hash() for photo in photo_index)
        to_delete = list()
        for photo in photo_index:
            photo_hash = photo.get_hash()
            if photo_hash in all_photo_hashes:
                all_photo_hashes.discard(photo_hash)
                continue
            to_delete.append(photo)
        for photo in to_delete:
            os.remove(photo.get_path())

        if len(to_delete) == 0:
            return photo_index

        new_photo_index = PhotoIndex(photo_index_photo_delegate)
        new_photo_index.load(photo_index_root_path)
        return new_photo_index

    def autosort_photos(self, photo_index):
        # Sorts all photos from photo_index into collection.
        # - photo comes from within collection:
        #   - with main tag meta data:
        #     -> move to '<collection>/<tagged_photos_root_folder>/<main_tag_photo_path>'
        #   - without main tag meta data:
        #     -> don't move photo
        # - photo comes from outside collection:
        #   - with main tag meta data:
        #     -> move to '<collection>/<tagged_photos_root_folder>/<main_tag_photo_path>'
        #   - without main tag meta data:
        #     -> move to '<collection>/<date-now>/<photo-path-within-index>'
        assert photo_index.root_path is not None
        assert self.collection_root is not None
        photo_index_root_path = photo_index.root_path
        timestamped_collection_root_path = os.path.join(
            self.collection_root,
            datetime.datetime.now().strftime("added-at-%Y-%m-%d_%H-%M-%S"),
        )

        def get_photo_index_subpath(path):
            assert path.startswith(photo_index_root_path)
            path_remainder, subpath = os.path.split(path)
            if path_remainder == photo_index_root_path:
                return subpath
            return os.path.join(get_photo_index_subpath(path_remainder), subpath)

        for photo in photo_index:
            # try to move photo based on main-tag information ...
            main_tag_photo_path = self._get_main_tag_photo_path(photo)
            if main_tag_photo_path is not None:
                photo.set_path(main_tag_photo_path)
                continue
            # ... if no main_tag_photo_path can be determined, check if photo is stored
            # within collection ...
            if photo.get_path().startswith(self.collection_root):
                continue
            # ... if not, move photo into collection.
            collection_photo_path = os.path.join(
                timestamped_collection_root_path,
                get_photo_index_subpath(photo.get_path()),
            )
            photo.set_path(collection_photo_path)

    def cleanup_and_integrate(self):
        assert self.photo_index.root_path is not None and self.meta_storage_manager is not None
        self.photo_index = self.delete_duplicate_photos(self.photo_index)
        self.meta_storage_manager.cleanup_and_migrate_meta_data_and_directories(self.photo_index)
        self.autosort_photos(self.photo_index)

    def get_list_of_all_tags(self):
        assert self.meta_storage_manager is not None
        meta_file_directories = self.meta_storage_manager.find_all_directories_with_meta_files()
        all_tags = set()
        for meta_file_directory in meta_file_directories:
            meta_storage = MetaStorage(meta_file_directory)
            hashes = MetaStorage(meta_file_directory).get_hashes()
            for hash in hashes:
                all_tags.update(meta_storage.get_meta(hash).get("tags", []))
        return sorted(all_tags)

    @staticmethod
    def _get_next_non_existing_path(path):
        new_path = path
        i = 0
        root, ext = os.path.splitext(path)
        while os.path.exists(new_path):
            root_base_match = re.match(r"^(.*?)(?:--\d+)?$", root)
            assert root_base_match is not None, "re.match failed for r\"^(.*?)(?:--\\d+)?$\" which is unexpected."
            root_base = root_base_match.group(1)
            i += 1
            new_path = f"{root_base}--{i}{ext}"
        assert not os.path.exists(new_path)
        return new_path

    def _get_main_tag_photo_path(self, photo):
        assert self.collection_root is not None
        assert isinstance(self.collection_settings.tagged_photos_root_folder, str)
        main_tag = photo.get_main_tag()
        if main_tag is None:
            return None
        
        return os.path.join(
            self.collection_root,
            self.collection_settings.tagged_photos_root_folder,  # might be empty string which os.path.join can handle properly
            *main_tag.split(":"),
            photo.get_filename(),
        )

    def hook_and_connect_photo_delegate(self, photo_delegate):
        class PhotoDelegateHooked(photo_delegate):

            #override
            @staticmethod
            def file_is_supported(path):
                assert self.collection_root is not None
                deleted_photos_folder = self.collection_settings.deleted_photos_folder
                assert isinstance(deleted_photos_folder, str)
                if deleted_photos_folder == "" or deleted_photos_folder is None:
                    return photo_delegate.file_is_supported(path)

                return (
                    photo_delegate.file_is_supported(path)
                    and not path.startswith(os.path.join(
                        self.collection_root,
                        deleted_photos_folder,
                    ))
                )

            #override
            def set_main_tag(_self, tag):
                assert self.collection_root is not None
                old_tag = _self.get_main_tag()
                super().set_main_tag(tag)
                new_path = self._get_main_tag_photo_path(_self)

                if new_path is None and old_tag is not None:
                    # The file was autosorted but should be moved into collection root
                    new_path = os.path.join(self.collection_root, _self.get_filename())

                if new_path is not None and _self.get_path() is not new_path:
                    # The file is in the wrong location
                    _self.set_path(new_path)

            #override
            def set_path(_self, path):
                assert self.meta_storage_manager is not None
                old_path = _self.get_path()
                if old_path == path:
                    return
                old_directory = os.path.dirname(old_path)
                new_directory = os.path.dirname(path)
                photo_hash = _self.get_hash()

                os.makedirs(new_directory, exist_ok=True)
                new_path = self._get_next_non_existing_path(path)
                _self._path = new_path
                shutil.move(old_path, new_path)
                self.meta_storage_manager.migrate_meta_data(photo_hash, old_directory, new_directory)
                self.meta_storage_manager._recursive_delete_empty_directories(old_directory)
        return PhotoDelegateHooked
