# SPDX-FileCopyrightText: 2023 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-2.0-only

from PySide6.QtCore import Qt
from PySide6.QtCore import QSize
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        self._pixmap = None
        self._pixmap_scaled = None

        self._aspect_ratio = Qt.AspectRatioMode.KeepAspectRatio
        self._size_hint = QSize()
        self._transformation_mode = Qt.TransformationMode.SmoothTransformation

    def _calc_pixmap_scaled(self):
        if self._pixmap:
            self._pixmap_scaled = self._pixmap.scaled(
                self.size(),
                self._aspect_ratio,
                self._transformation_mode,
            )
        self.update()

    def set_pixmap(self, pixmap):
        if self._pixmap == pixmap:
            return

        self._pixmap = pixmap
        if pixmap is None:
            self._size_hint = QSize(0, 0)
            return

        self._size_hint = pixmap.size()
        self._pixmap_scaled = pixmap.scaled(
            self.size(),
            self._aspect_ratio,
            self._transformation_mode,
        )

        self._calc_pixmap_scaled()
        self.updateGeometry()

    def set_aspect_ratio(self, aspect_ratio):
        if self._aspect_ratio == aspect_ratio:
            return
        self._aspect_ratio = aspect_ratio
        self._calc_pixmap_scaled()

    def set_transformation_mode(self, transformation_mode):
        if self._transformation_mode == transformation_mode:
            return
        self._transformation_mode = transformation_mode
        self._calc_pixmap_scaled()

    def sizeHint(self):
        return self._size_hint

    def resizeEvent(self, event):
        self._calc_pixmap_scaled()
        super().resizeEvent(event)

    def paintEvent(self, event):
        if self._pixmap_scaled is None:
            return
        painter = QPainter(self)
        pixmap_rect = self._pixmap_scaled.rect()
        pixmap_rect.moveCenter(self.rect().center())
        painter.drawPixmap(pixmap_rect, self._pixmap_scaled)
        super().paintEvent(event)
