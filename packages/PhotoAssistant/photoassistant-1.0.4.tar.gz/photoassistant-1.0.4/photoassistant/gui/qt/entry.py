# SPDX-FileCopyrightText: 2023 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-2.0-only

import datetime
import importlib.resources
import os
import re
import sys
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal as QSignal
from PySide6.QtGui import QAction
from PySide6.QtGui import QIcon
from PySide6.QtGui import QStandardItem
from PySide6.QtGui import QStandardItemModel
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QMenuBar
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QScrollArea
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QSplitter
from PySide6.QtWidgets import QStatusBar
from PySide6.QtWidgets import QTabWidget
from PySide6.QtWidgets import QTextEdit
from PySide6.QtWidgets import QWidget

from photoassistant.core.photocollection import PhotoCollectionManager
from photoassistant.gui.qt.photo import PhotoQt
from photoassistant.gui.qt.photodatamodel import PhotoDataModel
from photoassistant.gui.qt.photoview import PhotoAssistantPhotoView
from photoassistant.gui.qt.utils.qtutils import BusyIndicatorDialog
from photoassistant.gui.qt.utils.qtutils import ErrorQMessageBox
from photoassistant.gui.qt.utils.qtutils import InfoQMessageBox
from photoassistant.gui.qt.utils.qtutils import QComboBoxEditable
from photoassistant.gui.qt.utils.qtutils import QKeySequenceStandardKeyUtils
from photoassistant.gui.qt.utils.qtutils import QLabeledProperty
from photoassistant.gui.qt.utils.qtutils import QListWidgetTransparentMinimumSized
from photoassistant.gui.qt.utils.qtutils import QModernStyleGroupBox
from photoassistant.gui.qt.utils.qtutils import QModernStyleGroupBoxContainer
from photoassistant.gui.qt.utils.qtutils import QMarginContainer
from photoassistant.gui.qt.utils.qtutils import QSizePolicyStretch
from photoassistant.gui.qt.utils.qtutils import ScrollableInfoDialog
from photoassistant.gui.qt.utils.qtutils import SynchronizedExecution
from photoassistant.gui.qt.imageviewer import ImageViewer


class TagsModel(QStandardItemModel):
    def __init__(self):
        super().__init__()

    def set_tags(self, tags):
        self.clear()
        self.appendRow(QStandardItem(""))
        for tag in tags:
            self.appendRow(QStandardItem(tag))


class PhotoViewControlPanel(QWidget):
    sort_function_selected_signal = QSignal(str)
    apply_filters_signal = QSignal(list, list)

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        sort_combobox = QComboBox()
        sort_combobox.addItems(
            [
                "filename",
                "creation timestamp"
            ]
        )

        self.filter_include_text_input = QTextEdit()
        self.filter_include_text_input.setMinimumWidth(100)
        self.filter_include_text_input.setPlaceholderText(
            f"Every line adds a filter rule. "
            f"The following two lines filter photos that either have a tag including '2023' or have the tag 'city':{os.linesep}"
            f"*2023*{os.linesep}"
            f"city{os.linesep}"
        )
        self.filter_exclude_text_input = QTextEdit()
        self.filter_exclude_text_input.setMinimumWidth(100)
        self.filter_exclude_text_input.setPlaceholderText(
            f"Every line adds a filter rule. "
            f"The following two lines filter photos that do not have a tag including '2023' and do not have the tag 'city':{os.linesep}"
            f"*2023*{os.linesep}"
            f"city{os.linesep}"
        )

        apply_filters_button = QPushButton("Apply Tag Filters")
        apply_filters_button.clicked.connect(self._emit_apply_filters)

        apply_filters_button_layout = QGridLayout()
        apply_filters_button_layout.addWidget(apply_filters_button, 0, 1)
        apply_filters_button_layout.setColumnStretch(0, 1)
        apply_filters_button_layout.setColumnStretch(1, 18)
        apply_filters_button_layout.setColumnStretch(2, 1)


        sort_combobox.currentTextChanged.connect(self.sort_function_selected_signal.emit)

        grid_layout = QGridLayout(self)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.addWidget(QModernStyleGroupBoxContainer("Sort By", widget=sort_combobox), 0, 0)
        grid_layout.addWidget(QModernStyleGroupBoxContainer("Filter Photos With Tags", widget=self.filter_include_text_input), 1, 0)
        grid_layout.addWidget(QModernStyleGroupBoxContainer("Filter Photos Without Tags", widget=self.filter_exclude_text_input), 2, 0)
        grid_layout.addLayout(apply_filters_button_layout, 3, 0)

    def _emit_apply_filters(self):
        include_filter_tags = list()
        include_filter_text = self.filter_include_text_input.toPlainText()
        for line in include_filter_text.splitlines():
            line = line.strip()
            include_filter_tags.append(rf"^{line.replace('*', '.*')}$")

        exclude_filter_tags = list()
        exclude_filter_text = self.filter_exclude_text_input.toPlainText()
        for line in exclude_filter_text.splitlines():
            line = line.strip()
            exclude_filter_tags.append(rf"^{line.replace('*', '.*')}$")
        self.apply_filters_signal.emit(include_filter_tags, exclude_filter_tags)


class TagEntry(QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.setMinimumHeight(20)

        self.tag_entry = QComboBoxEditable(minimum_size=(100, 0))

        grid_layout = QGridLayout(self)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.addWidget(self.tag_entry, 0, 0)

    def set_model(self, model):
        if model is None:
            tag_entry_model = self.tag_entry.model()
            if isinstance(tag_entry_model, TagsModel):
                tag_entry_model.clear()
            return
        self.tag_entry.setModel(model)

    def _set_tag_items(self, tags):
        assert isinstance(tags, list)
        self.tag_entry.addItems(tags)

    def text(self):
        return self.tag_entry.currentText()


class TagGroup(QWidget):
    delete_signal = QSignal()

    class TagEntryWithDeleteButton(TagEntry):
        def __init__(self, parent=None, **kwargs):
            super().__init__(parent, **kwargs)
            self.tag_delete_button = QPushButton("X")
            self.tag_delete_button.setMinimumWidth(20)
            self.tag_delete_button.setMaximumWidth(40)

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.tags_model = None

        self.tag_entries = []
        self.grid_layout_tag_entries = QGridLayout()
        self.grid_layout_tag_entries.setContentsMargins(0, 0, 0, 0)

        add_tag_button = QPushButton("+")

        add_tag_button_layout = QGridLayout()
        add_tag_button_layout.addWidget(add_tag_button, 0, 1)
        add_tag_button_layout.setColumnStretch(0, 1)
        add_tag_button_layout.setColumnStretch(1, 1)
        add_tag_button_layout.setColumnStretch(2, 1)

        add_tag_button.clicked.connect(self.add_tag_entry)

        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.addLayout(self.grid_layout_tag_entries, 0, 0)
        self.grid_layout.addLayout(add_tag_button_layout, 1, 0)

        self.add_tag_entry()

    def set_model(self, model):
        self.tags_model = model
        for tag_entry in self.tag_entries:
            tag_entry.set_model(model)

    def add_tag_entry(self):
        tag_entry = self.TagEntryWithDeleteButton()
        tag_entry.set_model(self.tags_model)
        tag_index = len(self.tag_entries)
        self.tag_entries.append(tag_entry)
        self.grid_layout_tag_entries.addWidget(tag_entry, tag_index, 0)
        self.grid_layout_tag_entries.addWidget(tag_entry.tag_delete_button, tag_index, 1)

        tag_entry.tag_delete_button.clicked.connect(lambda: self.delete_tag_entry(tag_entry))

    def delete_tag_entry(self, tag_entry):
        tag_index = self.tag_entries.index(tag_entry)
        for i in reversed(range(tag_index, len(self.tag_entries))):
            tag_entry_widget = self.tag_entries[i]
            tag_entry_widget.setParent(None)
            tag_delete_button_widget = tag_entry_widget.tag_delete_button
            tag_delete_button_widget.setParent(None)
        self.tag_entries.pop(tag_index).deleteLater()
        for i, tag_entry in enumerate(self.tag_entries[tag_index:], tag_index):
            self.grid_layout_tag_entries.addWidget(tag_entry, i, 0)
            self.grid_layout_tag_entries.addWidget(tag_entry.tag_delete_button, i, 1)

        if len(self.tag_entries) == 0:
            self.delete_signal.emit()

    def get_tags(self):
        all_tags = []
        for tag_entry in self.tag_entries:
            tag_text = tag_entry.text().strip()
            if tag_text != "":
                all_tags.append(tag_text)
        return all_tags


class TagsPanel(QWidget):
    tags_updated_signal = QSignal()

    class TagGroupWithHeader(QModernStyleGroupBox):
        delete_signal = QSignal()

        def __init__(self, title="Tag Group X", parent=None):
            super().__init__(title, parent)

            self.apply_tag_group_button = QPushButton(f"Apply Tags")
            self.tag_group = TagGroup()

            grid_layout = QGridLayout(self)
            grid_layout.setContentsMargins(0, 0, 0, 0)
            grid_layout.addWidget(self.apply_tag_group_button, 0, 0)
            grid_layout.addWidget(self.tag_group, 1, 0)

            self.tag_group.delete_signal.connect(self.delete_signal.emit)

        def set_model(self, model):
            self.tag_group.set_model(model)

        def set_tag_group_index(self, index):
            self.setTitle(f"Tag Group {index}")
            self.apply_tag_group_button.setText(f"Apply Tags")

        def get_tags(self):
            return self.tag_group.get_tags()

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.tags_model = None

        self.tag_groups = []
        self.photos_selected = []

        self.grid_layout_tag_groups = QGridLayout()
        self.grid_layout_tag_groups.setContentsMargins(0, 0, 0, 0)

        add_tag_group_button = QPushButton("Add Tag Group")

        add_tag_group_button_layout = QGridLayout()
        add_tag_group_button_layout.addWidget(add_tag_group_button, 0, 1)
        add_tag_group_button_layout.setColumnStretch(0, 1)
        add_tag_group_button_layout.setColumnStretch(1, 18)
        add_tag_group_button_layout.setColumnStretch(2, 1)

        add_tag_group_button.clicked.connect(self.add_tag_group)

        grid_layout = QGridLayout(self)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.addLayout(self.grid_layout_tag_groups, 0, 0)
        grid_layout.addLayout(add_tag_group_button_layout, 1, 0)
        grid_layout.addItem(QSpacerItem(0, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), 2, 0)

        self.add_tag_group()

    def set_model(self, model):
        self.tags_model = model
        for tag_group in self.tag_groups:
            tag_group.set_model(model)

    def add_tag_group(self):
        tag_group = TagsPanel.TagGroupWithHeader()
        tag_group.set_model(self.tags_model)
        tag_group_index = len(self.tag_groups)
        tag_group.set_tag_group_index((tag_group_index + 1))
        self.tag_groups.append(tag_group)
        self.grid_layout_tag_groups.addWidget(tag_group, tag_group_index, 0)

        tag_group.delete_signal.connect(lambda: self.delete_tag_group(tag_group))
        tag_group.apply_tag_group_button.clicked.connect(lambda: self.apply_tags(tag_group_index))

    def delete_tag_group(self, tag_group):
        tag_group_index = self.tag_groups.index(tag_group)
        for i in reversed(range(tag_group_index, len(self.tag_groups))):
            tag_group = self.tag_groups[i]
            tag_group.setParent(None)
        self.tag_groups.pop(tag_group_index).deleteLater()
        for i, tag_group in enumerate(self.tag_groups[tag_group_index:], tag_group_index):
            self.grid_layout_tag_groups.addWidget(tag_group, i, 0)
            tag_group.set_tag_group_index((i + 1))

    def set_photos_selected(self, photos):
        self.photos_selected = photos

    def apply_tags(self, tag_group_index):
        if tag_group_index < 0 or tag_group_index >= len(self.tag_groups):
            return
        tags = self.tag_groups[tag_group_index].get_tags()
        main_tag = [tag for tag in tags if tag.startswith(":")]
        main_tag = None if len(main_tag) == 0 else main_tag[-1]
        tags = [tag for tag in tags if not tag.startswith(":")]
        for photo in self.photos_selected:
            if main_tag is not None:
                photo.set_main_tag(main_tag)
            for tag in tags:
                photo.add_tag(tag)
        self.tags_updated_signal.emit()


class PhotoInfoPanel(QWidget):
    class SinglePhotoInfo(QWidget):
        def __init__(self, parent=None, **kwargs):
            super().__init__(parent, **kwargs)

            self.photo = None

            self.directory_property = QLabeledProperty("File Location")
            self.filename_property = QLabeledProperty("Filename")
            self.creation_timestamp_property = QLabeledProperty("Creation Date")
            self.gps_coordinates_property = QLabeledProperty("GPS Coordinates")

            grid_layout = QGridLayout(self)
            grid_layout.setContentsMargins(0, 0, 0, 0)
            grid_layout.addWidget(self.directory_property, 0, 0)
            grid_layout.addWidget(self.filename_property, 1, 0)
            grid_layout.addWidget(self.creation_timestamp_property, 2, 0)
            grid_layout.addWidget(self.gps_coordinates_property, 3, 0)

            self.set_photo(None)

        def set_photo(self, photo):
            if photo is None:
                self.hide()
                return

            self.show()
            self.photo = photo
            self.directory_property.set_text(f"{os.path.dirname(photo.path)}")
            self.filename_property.set_text(f"{photo.filename}")
            self.creation_timestamp_property.set_text(f"{photo.creation_timestamp}")
            self.gps_coordinates_property.set_text(f"{' '.join(f'{val:.4f}' if val is not None else '?' for val in photo.gps_coordinates)}")

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.photos_selected = []

        self.single_photo_info = self.SinglePhotoInfo()
        self.tag_list_widget = QListWidgetTransparentMinimumSized(self)
        self.tag_list_widget.setMinimumSize(100, 50)
        tag_list_widget_container = QModernStyleGroupBoxContainer("Tags", widget=self.tag_list_widget)

        grid_layout = QGridLayout(self)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.addWidget(self.single_photo_info, 0, 0)
        grid_layout.addWidget(tag_list_widget_container, 1, 0)

    def set_photos_selected(self, photos):
        self.photos_selected = photos
        self.update_photo_info()

    def update_tag_list(self):
        self.tag_list_widget.clear()
        tags = set()
        for photo in self.photos_selected:
            tags.update(photo.get_all_tags())
        main_tags = [tag for tag in tags if tag.startswith(":")]
        tags = [tag for tag in tags if not tag.startswith(":")]
        for tag in sorted(main_tags):
            self.tag_list_widget.addItem(tag)
        for tag in sorted(tags):
            self.tag_list_widget.addItem(tag)

    def update_photo_info(self):
        self.single_photo_info.set_photo(self.photos_selected[0] if len(self.photos_selected) == 1 else None)
        self.update_tag_list()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Delete, Qt.Key.Key_Backspace):
            selected_tags = [item.text() for item in self.tag_list_widget.selectedItems()]
            main_tags = [tag for tag in selected_tags if tag.startswith(":")]
            tags = [tag for tag in selected_tags if not tag.startswith(":")]
            for photo in self.photos_selected:
                if photo.main_tag in main_tags:
                    photo.main_tag = None
                for tag in tags:
                    photo.delete_tag(tag)
            self.update_photo_info()
            return
        super().keyPressEvent(event)


class PhotoViewer(QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.photo = None

        self.image_viewer = ImageViewer()

        grid_layout = QGridLayout(self)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.addWidget(self.image_viewer, 0, 0)

    def update_photo(self, photo):
        self.photo = photo
        self.image_viewer.set_pixmap(photo.get_image(max_size=self.image_viewer.size(), query_ignore_cache=True))

    def set_photo(self, photo):
        self.update_photo(photo)
        self.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_photo(self.photo)


class PhotoSortFunctions:
    DATETIME_NONE = datetime.datetime.fromtimestamp(0)
    @staticmethod
    def filename(photo):
        return photo.get_filename()

    @staticmethod
    def creation_timestamp(photo):
        timestamp = photo.get_creation_timestamp()
        if timestamp is None:
            timestamp = PhotoSortFunctions.DATETIME_NONE
        return timestamp

class PhotoAssistant(QMainWindow):
    apply_tags_signal = QSignal(int)
    photo_updated_signal = QSignal(object)

    PHOTOS_SORT_FUNCTIONS = {
        "filename": PhotoSortFunctions.filename,
        "creation timestamp": PhotoSortFunctions.creation_timestamp,
    }

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        with importlib.resources.as_file(importlib.resources.files("photoassistant").joinpath("photoassistant-icon.ico")) as icon_path_:
            icon = QIcon(str(icon_path_.resolve()))

        self.setWindowTitle(self.__class__.__name__)
        self.setWindowIcon(icon)
        self.setMinimumSize(640, 480)

        # business logic initialization
        self.photo_collection = PhotoCollectionManager(PhotoQt)
        self.photo_index = None

        self.photo_data_model_qt = PhotoDataModel()
        self.tags_model_qt = TagsModel()

        self.photos_sort_key = "filename"
        self.photo_filters = ([], [])
        self.photos_selected = []

        # Special widgets:
        # - seperate photo viewer window
        # - permanent status bar widget
        # - busy indicator dialog
        photo_viewer = PhotoViewer()
        self.programm_status_info_label = QLabel()
        self.busy_indicator_dialog = BusyIndicatorDialog(self)
        self.busy_indicator_dialog.setMinimumWidth(self.minimumWidth())
        self.busy_indicator_dialog.setWindowIcon(icon)
        self.info_dialog = ScrollableInfoDialog()
        self.info_dialog.setMinimumSize(self.minimumSize())
        self.info_dialog.setWindowIcon(icon)

        # central widget 'PhotoView' (grid with photos)
        photo_view = PhotoAssistantPhotoView()
        photo_view.setModel(self.photo_data_model_qt)
        photo_view.setSizePolicy(QSizePolicyStretch(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred, stretch_horizontal=3, stretch_vertical=1))

        # side panel widgets
        photo_view_control_panel = PhotoViewControlPanel()

        photo_add_tags_panel = TagsPanel()
        photo_add_tags_panel.set_model(self.tags_model_qt)

        photo_add_tags_panel_scroll_container = QScrollArea()
        photo_add_tags_panel_scroll_container.setWidgetResizable(True)
        photo_add_tags_panel_scroll_container.setFrameShape(QFrame.Shape.NoFrame)
        photo_add_tags_panel_scroll_container.setWidget(photo_add_tags_panel)

        info_panel = PhotoInfoPanel()

        photo_control_panel = QTabWidget()
        photo_control_panel.setDocumentMode(True)

        photo_control_panel.addTab(photo_add_tags_panel_scroll_container, "Add Tags")
        photo_control_panel.addTab(photo_view_control_panel, "View Control")

        # side panel widgets go into a vertical splitter
        side_panel_splitter = QSplitter()
        side_panel_splitter.setHandleWidth(8)
        side_panel_splitter.setOrientation(Qt.Orientation.Vertical)
        side_panel_splitter.addWidget(photo_control_panel)
        side_panel_splitter.addWidget(info_panel)
        side_panel_splitter.setSizes([800, 200])

        # central widget and side panel go into a horizontal splitter
        main_splitter = QSplitter()
        main_splitter.setHandleWidth(8)
        main_splitter.setOrientation(Qt.Orientation.Horizontal)
        main_splitter.addWidget(photo_view)
        main_splitter.addWidget(side_panel_splitter)
        main_splitter.setSizes([1800, 200])

        # signals and slots
        photo_view_control_panel.sort_function_selected_signal.connect(self.sort_photos)
        photo_view_control_panel.apply_filters_signal.connect(self.filter_photos)
        photo_view.photos_selected_signal.connect(info_panel.set_photos_selected)
        photo_view.photos_selected_signal.connect(lambda photos: photo_viewer.update_photo(photos[0]) if len(photos) == 1 else None)
        photo_view.photos_selected_signal.connect(self.set_photos_selected)
        photo_view.photos_selected_signal.connect(photo_add_tags_panel.set_photos_selected)
        photo_view.photo_open_signal.connect(photo_viewer.set_photo)
        photo_view.photo_delete_signal.connect(self.delete_photo)
        photo_add_tags_panel.tags_updated_signal.connect(info_panel.update_photo_info)
        self.apply_tags_signal.connect(photo_add_tags_panel.apply_tags)
        self.photo_updated_signal.connect(photo_viewer.update_photo)

        self.setCentralWidget(QMarginContainer(widget=main_splitter, margin=(8, 8, 8, 8)))

        self._initialize_menu_bar()


    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            number_keys = (Qt.Key.Key_1, Qt.Key.Key_2, Qt.Key.Key_3, Qt.Key.Key_4, Qt.Key.Key_5, Qt.Key.Key_6, Qt.Key.Key_7, Qt.Key.Key_8, Qt.Key.Key_9)
            if event.key() in number_keys: 
                index = number_keys.index(event.key())
                self.apply_tags_signal.emit(index)
                return
            if event.key() == Qt.Key.Key_R:
                if len(self.photos_selected) == 1:
                    self.rotate_photo(self.photos_selected[0])
                return
        super().keyPressEvent(event)

    def closeEvent(self, event):
        QApplication.quit()

    def _initialize_menu_bar(self):
        create_photo_collection_action = QAction("Create Collection", self)
        create_photo_collection_action.setStatusTip("Create a new Collection.")
        open_photo_collection_action = QAction("Open &Collection", self)
        open_photo_collection_action.setStatusTip("Open an existing Collection.")
        self.open_photos_action = QAction("Open &Photos", self)
        self.open_photos_action.setStatusTip("Open photos.")
        self.open_photos_action.setEnabled(False)
        self.integrate_opened_photos_action = QAction("Integrate Opened Photos and Meta Data", self)
        self.integrate_opened_photos_action.setStatusTip("Integrate currently opened photos and their meta data.")
        self.integrate_opened_photos_action.setEnabled(False)

        open_settings_action = QAction("Settings", self)
        open_settings_action.setStatusTip("Get help on changing settings of PhotoAssistant.")

        show_photoassistant_introduction_action = QAction("PhotoAssistant Introduction", self)
        show_photoassistant_introduction_action.setStatusTip("Displays an introduction to PhotoAssistant.")

        show_getting_started_action = QAction("Getting Started", self)
        show_getting_started_action.setStatusTip("Display a \"Getting Started\" help page.")

        show_quick_reference_action = QAction("Quick Reference", self)
        show_quick_reference_action.setStatusTip("Display a \"Quick Reference\" page.")

        show_about_action = QAction("About", self)
        show_about_action.setStatusTip("Display an \"About\" page.")


        create_photo_collection_action.triggered.connect(self._choose_photo_collection_to_create)
        open_photo_collection_action.triggered.connect(self._choose_photo_collection_to_open)
        self.open_photos_action.triggered.connect(self._choose_photos_to_open)
        self.integrate_opened_photos_action.triggered.connect(self._confirm_integrate_opened_photos)
        open_settings_action.triggered.connect(self._open_settings)

        show_photoassistant_introduction_action.triggered.connect(self._display_photoassistant_introduction)
        show_getting_started_action.triggered.connect(self._display_getting_started)
        show_quick_reference_action.triggered.connect(self._display_quick_reference)
        show_about_action.triggered.connect(self._display_about)

        menu = QMenuBar(None)
        self.setMenuBar(menu)

        file_menu = menu.addMenu("&File")
        file_menu.addAction(create_photo_collection_action)
        file_menu.addAction(open_photo_collection_action)
        file_menu.addAction(self.open_photos_action)
        file_menu.addAction(self.integrate_opened_photos_action)
        file_menu.addAction(open_settings_action)

        help_menu = menu.addMenu("&Help")
        help_menu.addAction(show_photoassistant_introduction_action)
        help_menu.addAction(show_getting_started_action)
        help_menu.addAction(show_quick_reference_action)
        help_menu.addAction(show_about_action)

        status_bar = QStatusBar(self)
        status_bar.addPermanentWidget(self.programm_status_info_label)

        self.setStatusBar(status_bar)

    def set_photos_selected(self, photos):
        self.photos_selected = photos

    def create_photo_collection(self, directory):
        assert os.path.isdir(directory), f"The path {directory} does not exist. Please choose an existing path to create a Collection!"
        try:
            collection_root = PhotoCollectionManager.find_collection(directory)
        except PhotoCollectionManager.CollectionError as e:
            # Modify the message of the exception appending some more helpful information for the user.
            raise PhotoCollectionManager.CollectionError(f"{str(e)} Collections can not be nested. More information can be found in menu \"Help\"")
        assert collection_root is None, f"Collections can not be nested. The conflicting Collection is at '{collection_root}'. More information can be found in menu \"Help\""

        PhotoCollectionManager.create(directory)
        self.open_photo_collection(directory)

    def open_photo_collection(self, directory):
        # This function must be executed in a thread seperate from the main thread
        # -> Using self.busy_indicator_dialog.execute 

        assert os.path.isdir(directory), f"The path {directory} does not exist. Please choose an existing path to open a Collection!"
        collection_root = PhotoCollectionManager.find_collection(directory)
        assert collection_root is not None, f"Collection can not be found at '{directory}'. Please use the menu \"File\" to create a collection first! More information can be found in menu \"Help\""

        def _update_ui():
            self.open_photos_action.setEnabled(True)
            self.integrate_opened_photos_action.setEnabled(True)
            self.set_program_status_info_label_text()

            if directory != self.photo_collection.collection_root:
                InfoQMessageBox(self, f"The directory chosen ({directory}) is contained within a collection at '{self.photo_collection.collection_root}' which has been loaded instead.").exec()

        update_ui_event = SynchronizedExecution.execute_event_blocked(_update_ui)
        def _update_data():
            self.photo_collection.set_collection_root(directory)
            update_ui_event.set()

        self.busy_indicator_dialog.execute("Open photo collection.", _update_data)

    def _update_photo_index(self):
        # This function must be executed in a thread seperate from the main thread
        # -> Using self.busy_indicator_dialog.execute 

        def _update_data():
            if self.photo_collection.collection_root is None or self.photo_collection.photo_index.root_path is None:
                return  # decorator will return BusyIndicatorDialog.ExecuteResult(None)

            photo_index_copy = self.photo_collection.photo_index.copy()
            include_tag_patterns, exclude_tag_patterns = self.photo_filters

            def _tags_include_match(photo):
                if len(include_tag_patterns) == 0:
                    return True
                photo_tags = photo.get_all_tags()
                for include_tag_pattern in include_tag_patterns:
                    if any(re.match(include_tag_pattern, tag) for tag in photo_tags):
                        return True
                return False

            def _tags_exclude_match(photo):
                if len(exclude_tag_patterns) == 0:
                    return False
                photo_tags = photo.get_all_tags()
                for exclude_tag_pattern in exclude_tag_patterns:
                    if any(re.match(exclude_tag_pattern, tag) for tag in photo_tags):
                        return True
                return False

            if len(include_tag_patterns) > 0:
                photo_index_copy = self.busy_indicator_dialog.execute(
                    "Filter photos by list of include tags.",
                    lambda: [photo for photo in photo_index_copy if _tags_include_match(photo)],
                ).wait()

            if len(exclude_tag_patterns) > 0:
                photo_index_copy = self.busy_indicator_dialog.execute(
                    "Filter photos by list of exclude tags.",
                    lambda: [photo for photo in photo_index_copy if not _tags_exclude_match(photo)],
                ).wait()

            self.busy_indicator_dialog.execute(
                f"Sort photos by '{self.photos_sort_key}'. This might require reading the meta data of every photo and meta file once.",
                lambda: photo_index_copy.sort(key=self.PHOTOS_SORT_FUNCTIONS[self.photos_sort_key]),
            ).wait()

            self.photo_index = photo_index_copy

        self.busy_indicator_dialog.execute("Update opened photos.", _update_data).wait()

    def open_photos(self, path):
        # This function must be executed in a thread seperate from the main thread
        # -> Using self.busy_indicator_dialog.execute 

        assert self.photo_collection.collection_root is not None, "Photos can only be opened after a Collection is opened. Please open a Collection first! More information can be found in menu \"Help\""
        assert os.path.isdir(path), f"The path {path} does not exist. Please choose an existing path to open photos!"

        results_container = dict()
        def _update_ui():
            self.tags_model_qt.set_tags(results_container["all_tags"])
            self.photo_data_model_qt.set_photo_index(self.photo_index)
            self.set_program_status_info_label_text()

        update_ui_event = SynchronizedExecution.execute_event_blocked(_update_ui)
        def _update_data():
            num_directories = self.busy_indicator_dialog.execute(
                f"Prescan directory '{path}'.",
                lambda: len([elem for elem in os.walk(path)]),
            ).wait()
            self.busy_indicator_dialog.execute(
                f"Load photos from {num_directories} directories in '{path}'.",
                lambda: self.photo_collection.open_photos(path, sort_key=self.PHOTOS_SORT_FUNCTIONS["filename"])
            ).wait()
            num_photos = len(self.photo_collection.photo_index)
            results_container["all_tags"] = self.busy_indicator_dialog.execute(
                f"Read tags from {num_photos} photos.",
                self.photo_collection.get_list_of_all_tags,
            ).wait()
            self._update_photo_index()
            update_ui_event.set()

        self.busy_indicator_dialog.execute("Open photos.", _update_data)

    def integrate_opened_photos(self):
        assert self.photo_collection.collection_root is not None, "Photos can only be integrated after a Collection is opened. Please open a Collection first! More information can be found in menu \"Help\""
        assert self.photo_collection.photo_index.root_path is not None, "No photos for integration opened. Please open a photos first! More information can be found in menu \"Help\""

        def _update_ui():
            self.photo_data_model_qt.set_photo_index(self.photo_index)
            self.set_program_status_info_label_text()

        update_ui_event = SynchronizedExecution.execute_event_blocked(_update_ui)
        def _update_data():
            num_photos = len(self.photo_collection.photo_index)
            self.busy_indicator_dialog.execute(
                f"Analyze {num_photos} photos for integration.",
                lambda: self.photo_collection.cleanup_and_integrate(),
            ).wait()
            self._update_photo_index()
            update_ui_event.set()

        self.busy_indicator_dialog.execute("Integrate and cleanup opened photos.", _update_data)

    def sort_photos(self, sort_key="filename"):
        # This function must be executed in a thread seperate from the main thread
        # -> Using self.busy_indicator_dialog.execute 

        def _update_ui():
            self.photo_data_model_qt.set_photo_index(self.photo_index)
            self.set_program_status_info_label_text()

        update_ui_event = SynchronizedExecution.execute_event_blocked(_update_ui)
        def _update_data():
            assert sort_key in self.PHOTOS_SORT_FUNCTIONS
            self.photos_sort_key = sort_key
            self._update_photo_index()
            update_ui_event.set()

        self.busy_indicator_dialog.execute("Sort opened photos.", _update_data)

    def filter_photos(self, include_filter_tags, exclude_filter_tags):
        # This function must be executed in a thread seperate from the main thread
        # -> Using self.busy_indicator_dialog.execute 

        def _update_ui():
            self.photo_data_model_qt.set_photo_index(self.photo_index)
            self.set_program_status_info_label_text()

        update_ui_event = SynchronizedExecution.execute_event_blocked(_update_ui)
        def _update_data():
            self.photo_filters = (include_filter_tags, exclude_filter_tags)
            self._update_photo_index()
            update_ui_event.set()

        self.busy_indicator_dialog.execute("Filter opened photos.", _update_data)

    def rotate_photo(self, photo):
        with self.photo_data_model_qt.updating_photo(photo):
            orientation_correction = photo.get_orientation_correction()
            orientation_correction = [
                orientation_correction[3],
                orientation_correction[4],
                orientation_correction[5],
                -orientation_correction[0],
                -orientation_correction[1],
                -orientation_correction[2],
                orientation_correction[6],
                orientation_correction[7],
                orientation_correction[8],
            ]
            photo.set_orientation_correction(orientation_correction)
        self.photo_updated_signal.emit(photo)

    def delete_photo(self, photo):
        with self.photo_data_model_qt.removing_photo(photo):
            self.photo_collection.delete_photo(photo)
            # photo_data_model_qt.photo_index is a copy of photo_collection.photo_index
            # -> we must delete the photo here seperately.
            self.photo_data_model_qt.photo_index.remove(photo)

    def set_program_status_info_label_text(self):
        collection_root_str = f"Collection: '{self.photo_collection.collection_root}'"
        photos_str = "Photos: no photos loaded"
        if self.photo_index is not None and self.photo_index.root_path is not None:
            num_photos = len(self.photo_index)
            photos_str = f"Photos: '{self.photo_index.root_path}' ({num_photos} photos)"
        self.programm_status_info_label.setText(f"{collection_root_str} | {photos_str}")

    def _choose_photo_collection_to_create(self):
        directory = QFileDialog.getExistingDirectory(self, "Create a Collection:")
        if directory is None or directory == "":
            # cancelled operation
            return

        try:
            self.create_photo_collection(directory)
        except PhotoCollectionManager.CollectionError as e:
            ErrorQMessageBox(self, f"Error encountered during checks for collection creation: {e}").exec()
            return
        except AssertionError as e:
            ErrorQMessageBox(self, str(e)).exec()
            return

    def _choose_photo_collection_to_open(self):
        directory = QFileDialog.getExistingDirectory(self, "Open a Collection:")
        if directory is None or directory == "":
            # cancelled operation
            return

        try:
            self.open_photo_collection(directory)
        except PhotoCollectionManager.CollectionError as e:
            ErrorQMessageBox(self, f"Error encountered when trying to opening a collection at '{directory}': {e}").exec()
            return 
        except AssertionError as e:
            ErrorQMessageBox(self, str(e)).exec()
            return

    def _choose_photos_to_open(self):
        try:
            assert self.photo_collection.collection_root is not None, "Photos can only be opened after a Collection is opened. Please open a Collection first! More information can be found in menu \"Help\""
        except AssertionError as e:
            ErrorQMessageBox(self, str(e)).exec()
            return

        directory = QFileDialog.getExistingDirectory(self, "Open Photos:")
        if directory is None or directory == "":
            # cancelled operation
            return

        try:
            self.open_photos(directory)
        except AssertionError as e:
            ErrorQMessageBox(self, str(e)).exec()
            return

    def _confirm_integrate_opened_photos(self):
        try:
            assert self.photo_collection.collection_root is not None, "Photos can only be integrated after a Collection is opened. Please open a Collection first! More information can be found in menu \"Help\""
            assert self.photo_collection.photo_index.root_path is not None, "No photos for integration opened. Please open a photos first! More information can be found in menu \"Help\""
        except AssertionError as e:
            ErrorQMessageBox(self, str(e)).exec()
            return

        text = (
            f"This operation will:{os.linesep}"
            f"- delete duplicate photos within the opened photos{os.linesep}"
            f"- cleanup meta data which is stored among the opened photos{os.linesep}"
            f"- integrate opened photos into the currently opened collection{os.linesep}"
            f"{os.linesep}"
            f"The operation will likely take a little while.{os.linesep}"
        )
        info = InfoQMessageBox(self, text)
        info.setStandardButtons(info.StandardButton.Ok | info.StandardButton.Cancel)
        if info.exec() != info.StandardButton.Ok:
            return

        try:
            self.integrate_opened_photos()
        except AssertionError as e:
            ErrorQMessageBox(self, str(e)).exec()
            return

    def _get_readme_text(self, mark=None):
        text = ""
        with importlib.resources.as_file(importlib.resources.files("photoassistant").joinpath("README.md")) as readme_path:
            with open(readme_path.resolve()) as file_:
                text = file_.read()
        if mark is not None:
            text_match = re.search(rf"<!-- {mark}_START -->(.*)<!-- {mark}_END -->", text, re.DOTALL)
            if text_match is not None:
                text = text_match.group(1)

            with importlib.resources.as_file(importlib.resources.files("photoassistant").joinpath("photoassistant-icon.png")) as icon_path_:
                icon_path = str(icon_path_.resolve())

            text = re.sub(r"\[(.*?)\]\((http.*?)\)", lambda match: f"**{match.group(1)}** ({match.group(2)})", text)
            text = re.sub(r"!\[Image\]\(photoassistant/photoassistant-icon.png\)", lambda _: f"![Image]({icon_path})", text)
            for q_standard_key in [
                QKeySequence.StandardKey.ZoomIn,
                QKeySequence.StandardKey.ZoomOut,
            ]:

                key_tag = f"QKeySequence.StandardKey.{q_standard_key.name}"
                text = re.sub(rf"<!-- {key_tag}_START -->.*<!-- {key_tag}_END -->", lambda _: f"`{QKeySequenceStandardKeyUtils.get_user_string(q_standard_key)}`", text)
        return text.strip()

    def _open_settings(self):
        text = self._get_readme_text("SETTINGS_SECTION")
        self.info_dialog.set_markdown(text, title="PhotoAssistant - Settings")

    def _display_photoassistant_introduction(self):
        text = self._get_readme_text("PHOTOASSISTANT_INTRODUCTION_SECTION")
        self.info_dialog.set_markdown(text, title="PhotoAssistant - Introduction")

    def _display_getting_started(self):
        text = self._get_readme_text("GETTING_STARTED_SECTION")
        self.info_dialog.set_markdown(text, title="PhotoAssistant - Getting Started")

    def _display_quick_reference(self):
        text = self._get_readme_text("QUICK_REFERENCE_SECTION")
        self.info_dialog.set_markdown(text, title="PhotoAssistant - Quick Reference")

    def _display_about(self):
        text = self._get_readme_text("ABOUT_SECTION")
        self.info_dialog.set_markdown(text, title="PhotoAssistant - About")




def main():
    app = QApplication(sys.argv)

    photoassistant = PhotoAssistant()
    photoassistant.resize(photoassistant.minimumSize())
    photoassistant.show()

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
