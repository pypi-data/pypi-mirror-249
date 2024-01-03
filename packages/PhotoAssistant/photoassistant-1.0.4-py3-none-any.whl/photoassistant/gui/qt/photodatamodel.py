# SPDX-FileCopyrightText: 2023 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-2.0-only

import contextlib

from PySide6.QtCore import QAbstractListModel
from PySide6.QtCore import Qt
from PySide6.QtCore import QModelIndex


class PhotoDataModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.photo_index = []

    def set_photo_index(self, photo_index):
        self.beginResetModel()
        self.photo_index = photo_index
        self.endResetModel()

    @contextlib.contextmanager
    def updating_photo(self, photo):
        if photo not in self.photo_index:
            yield
            return
        index = self.photo_index.index(photo)
        try:
            yield
        finally:
            qmodel_index = self.index(index, index, QModelIndex())
            self.dataChanged.emit(qmodel_index, qmodel_index, [Qt.ItemDataRole.UserRole])

    @contextlib.contextmanager
    def removing_photo(self, photo):
        if photo not in self.photo_index:
            yield
            return
        index = self.photo_index.index(photo)
        try:
            self.beginRemoveRows(QModelIndex(), index, index)
            yield
        finally:
            self.endRemoveRows()

    def rowCount(self, parent=None):
        return len(self.photo_index)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        photo_object = self.photo_index[index.row()]
        # (Extracted from source code documentation at
        # src/widgets/intemviews/qstyleditemdelegate.cpp):
        # Role                             | Accepted Types
        # ---------------------------------+------------------------------------
        # # Qt::AccessibleDescriptionRole  | QString
        # # Qt::AccessibleTextRole         | QString
        # Qt::BackgroundRole               | QBrush
        # Qt::CheckStateRole               | Qt::CheckState
        # Qt::DecorationRole               | QIcon, QPixmap, QImage and QColor
        # Qt::DisplayRole                  | QString and types with a string
        #                                    representation
        # Qt::EditRole                     | See QItemEditorFactory for details
        # Qt::FontRole                     | QFont
        # Qt::SizeHintRole                 | QSize
        # # Qt::StatusTipRole              | ? 
        # Qt::TextAlignmentRole            | Qt::Alignment
        # Qt::ForegroundRole               | QBrush
        # # Qt::ToolTipRole                | ?
        # # Qt::WhatsThisRole              | ?

        # This model uses Qt::UserRole to pass a PhotoObject
        if role == Qt.ItemDataRole.DisplayRole:
            return photo_object.filename
        if role == Qt.ItemDataRole.UserRole:
            return photo_object
        # TODO other roles
        return None
