from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QLabel


class ClickableLabel(QLabel):
    clicked: pyqtSignal = pyqtSignal()

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)