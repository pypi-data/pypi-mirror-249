# SPDX-FileCopyrightText: 2023 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-2.0-only

import math

from PySide6.QtCore import QItemSelection
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QPoint
from PySide6.QtCore import QRect
from PySide6.QtCore import QRectF
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal as QSignal
from PySide6.QtGui import QKeySequence
from PySide6.QtGui import QPainter
from PySide6.QtGui import QRegion
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QStyle
from PySide6.QtWidgets import QStyleOptionViewItem
from PySide6.QtWidgets import QStylePainter

from photoassistant.utils.cachingutils import CacheState
from photoassistant.utils.delayutils import DelayedQueryManager
from photoassistant.gui.qt.photoviewitemdelegate import PhotoViewItemDelegate
from photoassistant.gui.qt.utils.qtutils import QKeySequenceStandardKeyUtils

class PhotoView(QAbstractItemView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._photo_tiles_per_row = 4
        self.photo_tiles_visible = (self.photo_tiles_per_row * 1)
        self.photo_tile_width = 100
        self.photo_tile_height = 100
        self.rect_photo_grid = None
        self.update_photo_tile_size()

        self.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        self.horizontalScrollBar().setRange(0, 0)
        self.verticalScrollBar().setRange(0, 0)
        self.setItemDelegate(PhotoViewItemDelegate(self))

        self.pixmap_query_manager = DelayedQueryManager()
        self.pixmap_query_manager.set_max_queries(100)

    @property
    def photo_tiles_per_row(self):
        return self._photo_tiles_per_row

    @photo_tiles_per_row.setter
    def photo_tiles_per_row(self, photo_tiles_per_row):
        if 0 < photo_tiles_per_row <= 10:
            self._photo_tiles_per_row = photo_tiles_per_row
            self.reset()

    def setItemDelegate(self, *args, **kwargs):
        super().setItemDelegate(*args, **kwargs)
        self.update_photo_tile_size()

    def update_photo_tile_size(self):
        self.photo_tile_width = (self.viewport().width() / self.photo_tiles_per_row)
        self.photo_tile_height = self.photo_tile_width
        if hasattr(self.itemDelegate(), "photo_view_text_height"):
            self.photo_tile_height += getattr(self.itemDelegate(), "photo_view_text_height")
        photo_tile_width = max(1, self.photo_tile_width)
        photo_tile_height = max(1, self.photo_tile_height)
        self.photo_load_max_size = QSize((1 << math.ceil(math.log2(photo_tile_width))), (1 << math.ceil(math.log2(photo_tile_height))))
        photo_tiles_per_column = math.ceil(self.viewport().height() / photo_tile_height)
        self.photo_tiles_visible = (self.photo_tiles_per_row * photo_tiles_per_column)

        model = self.model()
        if model is not None:
            model_index_0 = model.index(0, 0, self.rootIndex())
            photo_0 = model_index_0.data(Qt.ItemDataRole.UserRole)
            if hasattr(photo_0, "ASYNC_SHARED_CACHE_IMAGES"):
                photo_0.ASYNC_SHARED_CACHE_IMAGES.set_slots(10 * self.photo_tiles_visible)

    def update_rect_photo_grid(self):
        rect_last_photo_tile = self.rect_for_row((self.model().rowCount() - 1)).toRect()
        self.rect_photo_grid = QRect(0, 0, self.viewport().width(), rect_last_photo_tile.bottom())

    def visualRect(self, index):
        return self.viewport_rect_for_row(index.row()).toRect()

    def rect_for_row(self, row):
        photo_grid_row_index = int(row / self.photo_tiles_per_row)
        photo_grid_col_index = (row % self.photo_tiles_per_row)
        return QRectF(
            (photo_grid_col_index * self.photo_tile_width),
            (photo_grid_row_index * self.photo_tile_height),
            self.photo_tile_width,
            self.photo_tile_height,
        )

    def viewport_rect_for_row(self, row):
        rect = self.rect_for_row(row)
        return rect.translated(
            -self.horizontalScrollBar().value(),
            -self.verticalScrollBar().value(),
        )

    def isIndexHidden(self, index):
        return False # TODO ?

    def scrollTo(self, index, scroll_hint):
        view_rect = self.viewport().rect()
        item_rect = self.visualRect(index)

        if item_rect.left() < view_rect.left():
            offset = item_rect.left() - view_rect.left()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + offset)
        elif item_rect.right() > view_rect.right():
            offset = min(
                item_rect.right() - view_rect.right(),
                item_rect.left() - view_rect.left(),
            )
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + offset)

        if item_rect.top() < view_rect.top():
            offset = item_rect.top() - view_rect.top()
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + offset)
        elif item_rect.bottom() > view_rect.bottom():
            offset = min(
                item_rect.bottom() - view_rect.bottom(),
                item_rect.top() - view_rect.top(),
            )
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + offset)

        self.viewport().update()

    def photo_grid_position_at(self, point):
        photo_grid_row_index = int(point.y() / self.photo_tile_height)
        photo_grid_col_index = int(point.x() / self.photo_tile_width)
        return (photo_grid_col_index, photo_grid_row_index)

    def row_of_photo_grid_position(self, photo_grid_col_index, photo_grid_row_index):
        return (photo_grid_row_index * self.photo_tiles_per_row) + photo_grid_col_index

    def indexAt(self, point):
        photo_grid_point = QPoint(
            (point.x() + self.horizontalScrollBar().value()),
            (point.y() + self.verticalScrollBar().value()),
        )
        photo_grid_col_index, photo_grid_row_index = self.photo_grid_position_at(photo_grid_point)
        row = self.row_of_photo_grid_position(photo_grid_col_index, photo_grid_row_index)
        return self.model().index(row, 0, self.rootIndex())

    def moveCursor(self, cursor_action, modifiers):
        current_index = self.currentIndex()
        if not current_index.isValid():
            return QModelIndex()

        current_row = current_index.row()
        max_row = (self.model().rowCount() - 1)
        new_row = None

        if cursor_action == QAbstractItemView.CursorAction.MoveLeft and current_row > 0:
            new_row = (current_row - 1)
        if cursor_action == QAbstractItemView.CursorAction.MoveUp and current_row > 0:
            new_row = (current_row - self.photo_tiles_per_row)

        if cursor_action == QAbstractItemView.CursorAction.MoveRight and current_row < max_row:
            new_row = (current_row + 1)
        if cursor_action == QAbstractItemView.CursorAction.MoveDown and current_row < max_row:
            new_row = (current_row + self.photo_tiles_per_row)

        if new_row is None:
            return QModelIndex()

        new_row = max(0, min(max_row, new_row))
        return self.model().index(new_row, 0, self.rootIndex())

    def horizontalOffset(self):
        return self.horizontalScrollBar().value()

    def verticalOffset(self):
        return self.verticalScrollBar().value()
    
    def scrollContentsBy(self, dx, dy):
        self.scrollDirtyRegion(dx, dy)
        self.viewport().scroll(dx, dy)

    def setSelection(self, rect, flags):
        item_selection = QItemSelection()
        item_selection.select(
            self.indexAt(rect.topLeft()),
            self.indexAt(rect.bottomRight()),
        )
        self.selectionModel().select(item_selection, flags)

    def visualRegionForSelection(self, selection):
        region = QRegion()
        for item_selection_range in selection:
            for row in range(item_selection_range.top(), item_selection_range.bottom()):
                for column in range(item_selection_range.left(), item_selection_range.right()):
                    region += self.visualRect(
                        self.model().index(row, column, self.rootIndex()),
                    )
        return region

    def _preload_photo_image(self, row):
        model = self.model()
        index = model.index(row, 0, self.rootIndex())
        if not index.isValid():
            return
        photo = index.data(Qt.ItemDataRole.UserRole)
        cache_state = photo.get_image(max_size=self.photo_load_max_size, query_cache_state_only=True)
        if cache_state == CacheState.DATA_MISSING:
            # We need to issue a query once with a callback as soon as the image is ready

            def query_callback(_):
                model.dataChanged.emit(index, index, [Qt.ItemDataRole.UserRole])
                self.pixmap_query_manager.stop_query_if_pending(photo)

            self.pixmap_query_manager.start_query_if_none_pending(
                photo,
                lambda: photo.get_image(
                    max_size=self.photo_load_max_size,
                    query_callback=query_callback,
                    query_result_placeholder=None,
                )
            )

    def paintEvent(self, event):
        painter = QStylePainter(self.viewport())
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        photo_grid_rect = self.viewport().rect().translated(
            self.horizontalScrollBar().value(),
            self.verticalScrollBar().value(),
        ).normalized()
        tl_photo_grid_col_index, tl_photo_grid_row_index = self.photo_grid_position_at(photo_grid_rect.topLeft())
        br_photo_grid_col_index, br_photo_grid_row_index = self.photo_grid_position_at(photo_grid_rect.bottomRight())

        def _paint_rows(row_from, row_to):
            for row in range(row_from, (row_to + 1)):
                index = self.model().index(row, 0, self.rootIndex())
                if not index.isValid():
                    continue
                rect = self.viewport_rect_for_row(row)
                option = QStyleOptionViewItem()
                self.initViewItemOption(option)
                option.rect = rect.toRect()
                if self.selectionModel().isSelected(index):
                    option.state |= QStyle.StateFlag.State_Selected
                if self.currentIndex() == index:
                    option.state |= QStyle.StateFlag.State_HasFocus

                item_delegate = self.itemDelegateForIndex(index)
                if isinstance(item_delegate, PhotoViewItemDelegate):
                    photo = index.data(Qt.ItemDataRole.UserRole)
                    cache_state = photo.get_image(max_size=self.photo_load_max_size, query_cache_state_only=True)
                    pixmap = photo.get_image(max_size=self.photo_load_max_size) if cache_state == CacheState.DATA_READY else None
                    item_delegate.paint_with_pixmap(painter, option, index, pixmap)
                else:
                    item_delegate.paint(painter, option, index)

        row_from = self.row_of_photo_grid_position(tl_photo_grid_col_index, tl_photo_grid_row_index)
        row_to = self.row_of_photo_grid_position(br_photo_grid_col_index, br_photo_grid_row_index)

        num_preload_images = (row_to + 1 - row_from)

        self.pixmap_query_manager.set_max_queries(num_preload_images)
        for row in range(row_from, (row_to + 1)):
            self._preload_photo_image(row)

        extra_preload_images = self.photo_tiles_visible
        row_count = self.model().rowCount()
        num_preload_images = ((row_to + 1 - row_from) + (2 * extra_preload_images))
        self.pixmap_query_manager.set_max_queries(num_preload_images)
        for i in range(1, extra_preload_images):
            row_above = (row_from - i)
            row_below = (row_to + i)
            if row_above > 0:
                self._preload_photo_image(row_above)
            if row_below < row_count:
                self._preload_photo_image(row_below)

        _paint_rows(row_from, row_to)

    def update_view(self):
        self.update_photo_tile_size()
        self.update_rect_photo_grid()
        self.updateGeometries()

    def reset(self):
        super().reset()
        self.update_view()

    def resizeEvent(self, event):
        self.update_view()
        super().resizeEvent(event)

    def updateGeometries(self):
        self.horizontalScrollBar().setSingleStep(self.photo_tile_width)
        self.horizontalScrollBar().setPageStep(self.viewport().width())
        self.horizontalScrollBar().setRange(0, 0)
        self.verticalScrollBar().setSingleStep(self.photo_tile_height / 10)
        self.verticalScrollBar().setPageStep(self.viewport().height())
        self.verticalScrollBar().setRange(0, max(0, (self.rect_photo_grid.bottom() - self.viewport().height())))


class PhotoAssistantPhotoView(PhotoView):
    photos_selected_signal = QSignal(list)
    photo_open_signal = QSignal(object)
    photo_delete_signal = QSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.doubleClicked.connect(lambda index: self.photo_open_signal.emit(index.data(Qt.ItemDataRole.UserRole)))

    def selectionChanged(self, changed_selected, changed_deselected):
        # We need to get the list of all photos from selectionModel as the parameter
        # 'changed_selected' includes only the additionally selected photos
        selection_indices = self.selectionModel().selection().indexes()
        photos_selected = [index.data(Qt.ItemDataRole.UserRole) for index in selection_indices]
        self.photos_selected_signal.emit(photos_selected)

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key.Key_Enter, Qt.Key.Key_Return]:
            selection_indices = self.selectionModel().selection().indexes()
            if len(selection_indices) > 0:
                self.photo_open_signal.emit(selection_indices[0].data(Qt.ItemDataRole.UserRole))
        elif (
            event.matches(QKeySequence.StandardKey.ZoomIn)
            or (
                # Fix for windows: Key '+' is not mapped properly: event.key() should be 43 but has found to be 93.
                # Resort to nativeVirtualKey() with windows specific codes:
                # https://www.qtcentre.org/threads/68749-keys-map-(cross-platform)
                # https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes?redirectedfrom=MSDN
                "PLUS" in QKeySequenceStandardKeyUtils.get_user_string(QKeySequence.StandardKey.ZoomIn)
                and (event.nativeVirtualKey() == 0xbb)
            )
        ):
            self.photo_tiles_per_row -= 1
            return
        elif event.matches(QKeySequence.StandardKey.ZoomOut):
            self.photo_tiles_per_row += 1
            return
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() in (Qt.Key.Key_Delete, Qt.Key.Key_Backspace):
                # ATTENTION, DATA LOSS RISK DUE TO QT IMPLEMENTATION
                # Iteration over selected indices and emitting a delete signal for each
                # element could be implemented like this:
                #
                # selection_indices = self.selectionModel().selection().indexes()
                # for selection_index in selection_indices:
                #     self.photo_delete_signal.emit(selection_index.data(Qt.ItemDataRole.UserRole))
                #
                # But there are some Qt specific limitations/weaknesses that currently
                # and potentially forever will lead to the deletion of the wrong photos!
                #
                # - The selection_indices being fetched once, can change their data after
                # photos are deleted. Probably, the C++ implementation uses an array-like
                # data type and Python gets a reference to a memory that is not bound to
                # the actual data.
                # - A deepcopy does not work as Python can not pickle a QModelIndex.
                # - As the Qt implementation 'removeRows' can only be called for contiguous
                # ranges we cannot achieve the correct behavior within a single instruction
                # (beginRemoveRows, delete_photos_in_the_model, endReomveRows).
                # - Removing photos in reversed order currently works (supports assumption
                # of array-like implementation with reference to memory slots). But this
                # behavior wouldn't be guaranteed to not change in the future!
                # -> The only solution left is handling the consistency promise on our own such
                # that only the photos that are supposed to be deleted will be deleted!
                # -> Fetch all photos upfront in our own list which elements are bound to
                # the data such that we can rely on consistency and work through that list! 

                selection_indices = self.selectionModel().selection().indexes()
                photos_selected = [index.data(Qt.ItemDataRole.UserRole) for index in selection_indices]
                for photo in photos_selected:
                    self.photo_delete_signal.emit(photo)
                return
        super().keyPressEvent(event)
