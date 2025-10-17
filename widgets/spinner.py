from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QPen
import sys

class Spinner(QWidget):
    def __init__(self, parent=None, lines=12, line_length=10, line_width=3, radius=10):
        super().__init__(parent)
        self.lines = lines
        self.line_length = line_length
        self.line_width = line_width
        self.radius = radius
        self.angle = 0

        self.timer: QTimer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(100)  # speed of rotation

        self.setFixedSize((radius + line_length) * 2, (radius + line_length) * 2)

    def rotate(self):
        self.angle = (self.angle + 30) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)

        for i in range(self.lines):
            color = QColor(0, 0, 0)
            color.setAlphaF((i + 1) / self.lines)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(color)

            painter.save()
            painter.rotate(self.angle + i * (360 / self.lines))
            painter.drawRoundedRect(self.radius, -self.line_width // 2, self.line_length, self.line_width, 2, 2)
            painter.restore()
