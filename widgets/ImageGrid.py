from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QGridLayout

from utils.ImageUtils import open_file, get_thumbnail_path, page_size_limit, open_image
from widgets.ClickableLabel import ClickableLabel

image_height = 100
image_width = 150
image_spacing = 10

class ImageGrid(QWidget):
    def __init__(self, root_dir, image_paths, page_index):
        super().__init__()

        self.root_dir = root_dir
        self.image_paths = image_paths
        self.images_per_row = 6
        self.page_index = page_index

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

        start_index = self.page_index * page_size_limit
        end_index = start_index + page_size_limit
        page_image_paths = self.image_paths[start_index : end_index]

        # Create image labels
        row, col = 0, 0
        for i, image_path in enumerate(page_image_paths):
            thumbnail_path = get_thumbnail_path(self.root_dir, image_path)
            pixmap = QPixmap(thumbnail_path)

            # Scale to thumbnail
            pixmap = pixmap.scaled(image_width, image_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

            label = ClickableLabel()
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("border: 1px solid #ccc; padding: 4px;")

            label.setFixedSize(image_width, image_height)

            label.clicked.connect(lambda path=image_path: open_image(self.root_dir, path))

            self.image_widgets.append(label)
            self.grid_layout.addWidget(label, row, col)

            col += 1
            if col >= self.images_per_row:
                col = 0
                row += 1


