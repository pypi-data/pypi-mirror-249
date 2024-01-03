# SPDX-FileCopyrightText: 2023 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-2.0-only

import importlib.resources
import math

from PySide6.QtCore import QPoint
from PySide6.QtCore import QRect
from PySide6.QtCore import QRectF
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetricsF
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPalette
from PySide6.QtGui import QTextLayout
from PySide6.QtGui import QTextOption
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QCommonStyle
from PySide6.QtWidgets import QStyle
from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtWidgets import QStyleOptionViewItem

from photoassistant.gui.qt.utils.qtutils import QPixmapLoader


class PhotoViewItemDelegate(QStyledItemDelegate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app = QApplication.instance()
        assert isinstance(app, QApplication)

        self.photo_view_text_height = math.ceil(2 * QFontMetricsF(app.font()).lineSpacing())

        screen_dots_per_mm = app.primaryScreen().physicalDotsPerInch() / 25.4
        self.image_margin = int(1.2 * screen_dots_per_mm)

        with importlib.resources.as_file(importlib.resources.files("photoassistant.gui.resources").joinpath("icon-loading.png")) as icon_path:
            self.placeholder_pixmap = QPixmapLoader.load(str(icon_path.resolve()))

    def paint(self, painter, option, index):
        return self.paint_with_pixmap(painter, option, index)

    def paint_with_pixmap(self, painter, option, index, pixmap=None):
        painter.save()
        painter.setRenderHints(QPainter.RenderHints.Antialiasing)

        # init paint option, widget and style
        # this creates an OptionStyleOptionViewItem (opt) as is done in the
        # original function QStyledItemDelegate.paint such that we can reuse
        # some code:
        # - setClipRegion(...)
        # The entire widget in the original function would be drawn with
        # 'style.drawControl(QStyle.ControlElement.CE_ItemViewItem, opt, ...)'.
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        widget = option.widget
        style = widget.style()

        # The model data of different roles of 'index' is transferred into 'opt'
        # as following:
        # (Extracted from source code documentation at
        # src/widgets/intemviews/qstyleditemdelegate.cpp):
        # option                        | Role                  | Accepted Types
        # ------------------------------+-----------------------+---------------
        # opt->backgroundBrush          | Qt::BackgroundRole    | QBrush
        # opt->features | HasCheckInd...| Qt::CheckStateRole    | Qt::CheckState
        # opt->checkState               |                       |
        # opt->features | HasDecoration | Qt::DecorationRole    | QIcon,QPixmap,
        # opt->icon                     |                       | QImage and
        # opt->decorationSize           |                       | QColor
        # opt->features | HasDisplay    | Qt::DisplayRole       | QString and
        # opt->text                     |                       | types with a
        #                               |                       | string repr
        # opt->font                     | Qt::FontRole          | QFont
        # opt->fontMetrics              |                       |
        # opt->displayAlignment         | Qt::TextAlignmentRole | Qt::Alignment
        # opt->palette.brush[:,Text]    | Qt::ForegroundRole    | QBrush

        # intersect clipping regions of painter and option
        if painter.hasClipping():
            painter.setClipRegion(painter.clipRegion().intersected(opt.rect))
        else:
            painter.setClipRegion(opt.rect)

        image_rect = option.rect.adjusted(
            self.image_margin,
            self.image_margin,
            -self.image_margin,
            -(self.image_margin + self.photo_view_text_height),
        )
        text_rect = QRect(
            image_rect.x(),
            (image_rect.bottom() + (self.image_margin >> 1)),
            image_rect.width(),
            self.photo_view_text_height,
        )
        selected_highlight_rect = option.rect if opt.showDecorationSelected else text_rect

        color_group = QPalette.ColorGroup.Disabled
        if QStyle.StateFlag.State_Enabled in opt.state:
            if QStyle.StateFlag.State_Active not in opt.state:
                color_group = QPalette.ColorGroup.Inactive
            else:
                color_group = QPalette.ColorGroup.Normal

        # draw background
        if QStyle.StateFlag.State_Selected in opt.state:
            painter.fillRect(selected_highlight_rect, opt.palette.brush(color_group, QPalette.ColorRole.Highlight))

        # draw image
        photo_object = index.data(Qt.ItemDataRole.UserRole)
        if photo_object:
            if pixmap is None:
                pixmap = self.placeholder_pixmap

            if pixmap:
                pixmap = pixmap.scaled(
                    image_rect.width(),
                    image_rect.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                )
                pixmap_rect = QRectF(
                    image_rect.x() + ((image_rect.width() - pixmap.width()) / 2),
                    image_rect.y() + ((image_rect.height() - pixmap.height()) / 2),
                    pixmap.width(),
                    pixmap.height(),
                ).toRect()
                painter.drawPixmap(pixmap_rect, pixmap)

        # draw filename of image (text)
        if QStyleOptionViewItem.ViewItemFeature.HasDisplay in opt.features and opt.text:
            if QStyle.StateFlag.State_Selected in opt.state:
                painter.setPen(opt.palette.color(color_group, QPalette.ColorRole.HighlightedText))
            else:
                painter.setPen(opt.palette.color(color_group, QPalette.ColorRole.Text))

            if QStyle.StateFlag.State_Editing in opt.state:
                painter.setPen(opt.palette.color(color_group, QPalette.ColorRole.Text))
                painter.drawRect(text_rect.adjusted(0, 0, -1, -1))

            text_margin = style.pixelMetric(QCommonStyle.PixelMetric.PM_FocusFrameHMargin, None, widget)
            text_rect = text_rect.adjusted(text_margin, 0, -text_margin, 0)

            text_option = QTextOption()
            text_option.setWrapMode(QTextOption.WrapMode.WrapAnywhere)
            text_option.setTextDirection(opt.direction)
            text_option.setAlignment(QStyle.visualAlignment(opt.direction, opt.displayAlignment))

            path_text = str(opt.text)
            text_layout = QTextLayout(path_text, opt.font)
            text_layout.setTextOption(text_option)

            line_width = text_rect.width()
            line_height = opt.fontMetrics.lineSpacing()
            text_draw_pos = text_rect.topLeft()

            text_layout.beginLayout()
            while True:
                line = text_layout.createLine()
                if not line.isValid():
                    break
                line.setLineWidth(line_width)
                if (text_draw_pos.y() + line_height) < text_rect.bottom():
                    line.draw(painter, text_draw_pos)
                    text_draw_pos += QPoint(0, line_height)
                else:
                    elided_last_line_path_text = opt.fontMetrics.elidedText(
                        path_text[line.textStart():],
                        Qt.TextElideMode.ElideRight,
                        text_rect.width(),
                    )
                    text_draw_pos += QPoint(0, opt.fontMetrics.ascent())
                    painter.drawText(
                        text_draw_pos,
                        elided_last_line_path_text,
                    )
                    break
            text_layout.endLayout()

        painter.restore()
