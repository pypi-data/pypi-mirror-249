# SPDX-FileCopyrightText: 2023 Anthony Zimmermann
#
# SPDX-License-Identifier: GPL-2.0-only

import importlib.resources
import logging
import math
import threading
import time

from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFontMetrics
from PySide6.QtGui import QImageReader
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QTransform
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QGroupBox
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QProgressBar
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QTextEdit
from PySide6.QtWidgets import QWidget

from photoassistant.utils.descriptors import RWDescriptor
from photoassistant.utils.descriptors import Signal


class SynchronizedExecution:
    @staticmethod
    def execute_event_blocked(function, event=None, polling_interval_ms=100):
        timer = QTimer()
        if event is None:
            event = threading.Event()
        def _try_execute():
            event.wait(timeout=0.001)
            if event.is_set():
                function()
                timer.stop()
        timer.timeout.connect(_try_execute)
        timer.start(polling_interval_ms)
        return event

    @staticmethod
    def execute_delayed(function, delay_ms=0):
        QTimer.singleShot(delay_ms, function)


class QKeySequenceStandardKeyUtils:
    @staticmethod
    def get_user_string(q_standard_key):
        user_string = QKeySequence(q_standard_key).toString().upper()
        def replace_keys(user_string_part, replacements):
            for orig, repl in replacements.items():
                if user_string_part.startswith(orig):
                    user_string_part = repl + user_string_part[len(orig):]
                    break
            parts = user_string_part.split("+", 1)
            if len(parts) == 1:
                return parts[0]
            return "+".join((parts[0], replace_keys(parts[1], replacements)))
        return replace_keys(
            user_string,
            {
                "+": "PLUS",
                "-": "MINUS"
            },
        )


class QSizePolicyStretch(QSizePolicy):
    def __init__(self, horizontal, vertical, stretch_horizontal=1, stretch_vertical=1):
        super().__init__(horizontal, vertical)
        self.setHorizontalStretch(stretch_horizontal)
        self.setVerticalStretch(stretch_vertical)


class QComboBoxEditable(QComboBox):
    def __init__(self, minimum_size=(100, 20), **kwargs):
        super().__init__(**kwargs)
        self.setEditable(True)
        self.setMinimumSize(*minimum_size)


class QListWidgetTransparentMinimumSized(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewport().setAutoFillBackground(False)
        self.setFrameShape(QFrame.Shape.NoFrame)

    def minimumSizeHint(self):
        return self.minimumSize()


class QTextEditResizing(QTextEdit):
    def __init__(self, parent=None, max_height_lines=4.1):
        super().__init__(parent)
        self._max_height_lines = max_height_lines

        self.setContentsMargins(0, 0, 0, 0)
        self.document().setDocumentMargin(0.0)

        size_policy = self.sizePolicy()
        size_policy.setHeightForWidth(True)
        size_policy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
        self.setSizePolicy(size_policy)

        self.textChanged.connect(self.updateGeometry)

    def resizeEvent(self, event):
        contents_margins = self.contentsMargins()
        self.setMinimumWidth(50 + contents_margins.left() + contents_margins.right())
        self.updateGeometry()
        super().resizeEvent(event)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        margins = self.contentsMargins()

        document_width = max(0, (width - margins.left() - margins.right()))
        document = self.document().clone()
        document.setTextWidth(document_width)
        full_height = math.ceil(margins.top() + document.size().height() + margins.bottom())
        max_height = math.ceil(
            margins.top()
            + (2 * document.documentMargin())
            + margins.bottom()
            + (self._max_height_lines * QFontMetrics(document.defaultFont()).lineSpacing())
        )
        return min(full_height, max_height)

    def minimumSizeHint(self):
        # self.ensurePolished()  # this function is implicitly called in super().sizeHint()
        width = super().sizeHint().width()
        return QSize(width, self.heightForWidth(self.width()))

    def sizeHint(self):
        return self.minimumSizeHint()


class QModernStyleGroupBox(QGroupBox):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setStyleSheet(
            "QGroupBox {"
            "border: 1px solid gray;"
            "border-radius: 0.5ex;"
            "margin-top: 0.6em;"
            "padding: 0.4em 2px 2px 2px;"
            "background-color: transparent;"
            "}"
            "QGroupBox::title {"
            "subcontrol-origin: margin;"
            "subcontrol-position: top left;"
            "padding: 0 3px 0 3px;"
            "left: 1.5ex;"
            "}"
        )


class QModernStyleGroupBoxContainer(QModernStyleGroupBox):
    def __init__(self, title, widget=None, parent=None):
        super().__init__(title, parent)

        self._grid_layout = QGridLayout(self)
        self._grid_layout.setContentsMargins(0, 0, 0, 0)

        if widget is not None:
            self._grid_layout.addWidget(widget)


class QLabeledProperty(QModernStyleGroupBoxContainer):
    class QLabeledPropertyLabel(QTextEditResizing):
        def __init__(self, parent=None, max_height_lines=4.1):
            super().__init__(parent, max_height_lines)

            self.setReadOnly(True)
            self.setFrameStyle(QFrame.Shape.NoFrame)
            self.viewport().setAutoFillBackground(False)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        def wheelEvent(self, event):
            if not (self.textInteractionFlags() & Qt.TextInteractionFlag.TextEditable):
                if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                    return
            super().wheelEvent(event)

        def focusOutEvent(self, event):
            cursor = self.textCursor()
            cursor.clearSelection()
            self.setTextCursor(cursor)
            super().focusOutEvent(event)


    def __init__(self, title, parent=None):
        super().__init__(title, parent)

        self.setFlat(True)
        self._property_label = self.QLabeledPropertyLabel()

        self.layout().addWidget(self._property_label, 0, 0)

    def set_text(self, text):
        self._property_label.setText(text)


class QMarginContainer(QWidget):
    def __init__(self, parent=None, widget=None, margin=(0, 0, 0, 0)):
        super().__init__(parent)

        self.setLayout(QGridLayout())

        self._widget = None
        self.set_margin(*margin)
        self.set_widget(widget)

    def set_margin(self, left, top, right, bottom):
        self.layout().setContentsMargins(left, top, right, bottom)

    def set_widget(self, widget):
        if widget == self._widget:
            return
        if self._widget is not None:
            self._widget.setParent(None)
        self._widget = widget
        self.layout().addWidget(self._widget, 0, 0)


class QPixmapLoader:
    @staticmethod
    def load(path, max_size=None, orientation_correction=None):
        try:
            reader = QImageReader(path)
            if max_size is not None:
                reader.setScaledSize(
                    reader.size().scaled(
                        max_size,
                        Qt.AspectRatioMode.KeepAspectRatio,
                    )
                )
            image = reader.read()
        except Exception:
            logging.getLogger(__name__).exception(f"Processing file '{path}' for image data failed")
            with importlib.resources.as_file(importlib.resources.files("gui.resources").joinpath("icon-broken-image.png")) as icon_path:
                return QPixmapLoader.load(str(icon_path.resolve()))

        if orientation_correction is not None:
            # We don't need to implement transformation into center and back
            # around the orientation_correction as the function QImage.transformed
            # will implicitly correct the transformation matrix to compensate for
            # transformations that move the center of the resulting image.
            q_transform = QTransform(
                orientation_correction[0],
                orientation_correction[3],
                orientation_correction[6],
                orientation_correction[1],
                orientation_correction[4],
                orientation_correction[6],
                orientation_correction[2],
                orientation_correction[5],
                orientation_correction[8],
            )
            image = image.transformed(q_transform)
        return QPixmap.fromImage(image)


class SimpleQMessageBox(QMessageBox):
    ICON = None
    BUTTON = QMessageBox.StandardButton.Ok
    def __init__(self, parent, message, title="INFO"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setText(message)
        self.setStandardButtons(self.BUTTON)
        if self.ICON is not None:
            self.setIcon(self.ICON)


class InfoQMessageBox(SimpleQMessageBox):
    ICON = QMessageBox.Icon.Information


class ErrorQMessageBox(SimpleQMessageBox):
    def __init__(self, parent, message, title="ERROR"):
        super().__init__(parent, message, title)
    ICON = QMessageBox.Icon.Critical


class ScrollableInfoDialog(QDialog):
    def __init__(self, parent=None, message="", title="PhotoAssistant"):
        super().__init__(parent)

        self.text_edit = QTextEdit()
        self.text_edit.setMarkdown(message)
        self.text_edit.setReadOnly(True)

        close_button = QPushButton("close")

        close_button_layout = QGridLayout()
        close_button_layout.addWidget(close_button, 0, 1)
        close_button_layout.setColumnStretch(0, 1)
        close_button_layout.setColumnStretch(1, 1)
        close_button_layout.setColumnStretch(2, 1)

        close_button.clicked.connect(self.hide)

        grid_layout = QGridLayout(self)
        grid_layout.addWidget(self.text_edit, 0, 0)
        grid_layout.addLayout(close_button_layout, 1, 0)

    def set_text(self, text, title="PhotoAssistant"):
        self.setWindowTitle(title)
        self.text_edit.setText(text)
        self.show()

    def set_markdown(self, text, title="PhotoAssistant"):
        self.setWindowTitle(title)
        self.text_edit.setMarkdown(text)
        self.show()


class BusyIndicatorDialog(QDialog):
    SHOW_DELAY = 0.5 # in seconds

    class ExecuteResult:
        NONE = object()
        data = RWDescriptor()

        def __init__(self, data=NONE):
            self._data_lock = threading.Lock()
            self._data_ready_event = threading.Event()
            self._data = None
            if data is not BusyIndicatorDialog.ExecuteResult.NONE:
                self.set_data(data)

        def get_data(self):
            with self._data_lock:
                return self._data

        def set_data(self, data):
            with self._data_lock:
                self._data = data
            self._data_ready_event.set()

        def is_ready(self):
            return self._data_ready_event.is_set()

        def wait(self, *args, **kwargs):
            self._data_ready_event.wait(*args, **kwargs)
            return self.data

    class MessageUpdateModule(threading.Thread):
        update_signal = Signal()
        MINIMUM_MESSAGE_DISPLAY_TIME = 3 # in seconds

        def __init__(self, start_delay, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.start_delay = start_delay

            self._message_queue = []
            self._message_queue_lock = threading.Lock()
            self._message_event = threading.Event()
            self._stop_event = threading.Event()

        def run(self):
            time.sleep(self.start_delay)
            while True:
                self._message_event.wait()
                if self._stop_event.is_set():
                    self._cleanup()
                    return
                with self._message_queue_lock:
                    if len(self._message_queue) == 0:
                        self._message_event.clear()
                        continue
                    self.update_signal.emit(self._message_queue.pop(0))
                time.sleep(self.MINIMUM_MESSAGE_DISPLAY_TIME)

        def stop(self):
            # First, set _stop_event such that the thread loop (run) will call
            # _cleanup() when _message_event is set.
            # Afterwards, set _message_event to release the
            # _message_event.wait which is maybe currently being executed.
            self._stop_event.set()
            self._message_event.set() # release wait on _message_event

        def add_message(self, message):
            with self._message_queue_lock:
                self._message_queue.append(message)
            self._message_event.set()

        def _cleanup(self):
            # delete all messages from the _message_queue and clear events
            with self._message_queue_lock:
                self._message_queue = []
            self._stop_event.clear()
            self._message_event.clear()

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("PhotoAssistant is running an operation that might take a while ...")
        self.setModal(True)

        self.info_label = QLabel()

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)

        grid_layout = QGridLayout(self)
        grid_layout.addWidget(self.info_label)
        grid_layout.addWidget(self.progress_bar)

        self.execute_thread_lock = threading.RLock()
        self.execute_thread = None
        self.message_update_module = None

        self.block_closing = True

    def execute(self, message, func, *args, **kwargs):
        # start one thread which picks up the messages to show and displays them
        # for at least MINIMUM_MESSAGE_DISPLAY_TIME in seconds
        with self.execute_thread_lock:
            if self.execute_thread is not None:
                self.set_message(message)
                return self.ExecuteResult(func(*args, **kwargs))

        self.info_label.setText(message)
        execute_result = self.ExecuteResult()
        def _target():
            with self.execute_thread_lock:
                self.message_update_module = self.MessageUpdateModule(self.SHOW_DELAY)
                self.message_update_module.update_signal.connect(self._show_message)

                self.message_update_module.start()
                execute_result.data = func(*args, **kwargs)
                self.message_update_module.stop()

                # clear references to execute_thead and message_update_module
                # such that the BusyIndicatorDialog is ready for starting the next
                # execution
                self.execute_thread = None
                self.message_update_module = None
        self.execute_thread = threading.Thread(target=_target)
        self.execute_thread.start()
        self._show_dialog(execute_result._data_ready_event)
        return execute_result

    def _show_message(self, message):
        self.info_label.setText(message)

    def _show_dialog(self, execute_result_ready_event):
        def _show_dialog_if_still_executing():
            if self.execute_thread is not None:
                super(self.__class__, self).show()
                SynchronizedExecution.execute_event_blocked(super(self.__class__, self).hide, event=execute_result_ready_event)
        SynchronizedExecution.execute_delayed(_show_dialog_if_still_executing, delay_ms=int(self.SHOW_DELAY * 1000))

    def set_message(self, message):
        if self.message_update_module is not None:
            self.message_update_module.add_message(message)

    # from PySide6 documentation: "In order to modify your dialog’s close behavior,
    # you can reimplement the functions accept() , reject() or done()"
    def accept(self):
        if not self.block_closing: super().accept()

    # from PySide6 documentation: "In order to modify your dialog’s close behavior,
    # you can reimplement the functions accept() , reject() or done()"
    def reject(self):
        if not self.block_closing: super().reject()

    # from PySide6 documentation: "In order to modify your dialog’s close behavior,
    # you can reimplement the functions accept() , reject() or done()"
    def done(self, result):
        if not self.block_closing: super().done(result)
