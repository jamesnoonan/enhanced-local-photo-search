import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QGridLayout

from utils.ImageUtils import open_image
from widgets.ClickableLabel import ClickableLabel

image_height = 100
image_width = 150
image_spacing = 10



class ImageGrid(QWidget):
    def __init__(self, image_paths):
        super().__init__()
        self.image_paths = image_paths
        self.images_per_row = 4
        self.image_widgets = []
        self.grid_layout = None

        self.init_ui()

    def init_ui(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(image_spacing)

        self.load_images()

        self.setLayout(self.grid_layout)

    def load_images(self):
        self.image_widgets = []



        # Create image labels
        row, col = 0, 0
        for i, image_path in enumerate(self.image_paths):
            pixmap = QPixmap(image_path)

            # Scale to thumbnail
            pixmap = pixmap.scaled(image_width, image_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

            label = ClickableLabel()
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("border: 1px solid #ccc; padding: 4px;")

            label.setFixedSize(image_width, image_height)

            label.clicked.connect(lambda path=image_path: open_image(path))

            self.image_widgets.append(label)
            self.grid_layout.addWidget(label, row, col)

            col += 1
            if col >= self.images_per_row:
                col = 0
                row += 1

    def update_grid(self, parent_width):
        # pass
        # Calculate how many images fit per row
        new_images_per_row = (parent_width - 50) / (image_width + image_spacing)
        new_images_per_row = max(1, math.floor(new_images_per_row))

        if new_images_per_row != self.images_per_row:
            print(f"Updating grid layout: {self.images_per_row} → {new_images_per_row}")
            self.images_per_row = new_images_per_row

            layout = self.grid_layout
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        layout.removeWidget(widget)

            # row, col = 0, 0
            # for label in self.image_widgets:
            #     layout.addWidget(label, row, col)
            #     col += 1
            #     if col >= self.images_per_row:
            #         col = 0
            #         row += 1

            self.load_images()
            layout.update()  # Repaints and may recalc sizes
            layout.invalidate()  # Marks the layout as dirty; next event loop pass will recompute

            self.update()
            self.setLayout(layout)
