import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel

image_height = 150
image_width = 150

images_per_row = 4

class ImageGrid(QWidget):
    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(10)

        # List image files
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp', '.tif', '.tiff')
        files = [
            f for f in os.listdir(self.folder_path)
            if f.lower().endswith(image_extensions)
        ]

        # Create image labels
        row, col = 0, 0
        for i, file in enumerate(files):
            image_path = os.path.join(self.folder_path, file)
            pixmap = QPixmap(image_path)

            # Scale to thumbnail
            pixmap = pixmap.scaled(image_width, image_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

            label = QLabel()
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("border: 1px solid #ccc; padding: 4px;")

            layout.addWidget(label, row, col)

            col += 1
            if col >= images_per_row:
                col = 0
                row += 1

        self.setLayout(layout)

    def update_grid(self):
      pass

    def resizeEvent(self, event):
        """Handle window resize to rearrange grid."""
        super().resizeEvent(event)
        self.update_grid()