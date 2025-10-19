import os

from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLabel

from utils.ImageUtils import collect_images, thumbnail_dir_name
from utils.SearchUtils import index_images
from widgets.ImageGrid import ImageGrid, image_limit
from widgets.TopRow import TopRow

class SearchView(QWidget):
    def __init__(self, folder_path):
        super().__init__()

        self.scroll_area = None
        self.image_grid = None
        self.folder_path = folder_path
        self.index = index_images(folder_path)

        self.image_paths = []
        self.init_ui()

    def init_ui(self):
        top_row = TopRow(self.on_search)
        images = collect_images(self.folder_path)

        self.scroll_area = QScrollArea()
        self.image_grid = ImageGrid(images)
        self.scroll_area.setWidget(self.image_grid)

        window_layout = QVBoxLayout()
        window_layout.addWidget(top_row)
        if len(images) > image_limit:
            label = QLabel(f"Results are limited to the first {image_limit} images")
            window_layout.addWidget(label)
        window_layout.addWidget(self.scroll_area)

        self.setLayout(window_layout)

    def on_search(self, search_string):
        image_paths = []

        if len(search_string.strip()) == 0:
            image_paths = list(map(lambda image: image["path"], self.index))
        else:
            search_terms = search_string.lower().split()

            for entry in self.index:
                filename = entry["filename"]
                caption = entry["caption"]

                for search_term in search_terms:
                    if search_term in filename or search_term in caption:
                        image_paths.append(entry["path"])
                        break

        self.image_grid = ImageGrid(image_paths)
        self.scroll_area.setWidget(self.image_grid)

    def resizeEvent(self, event):
        """Handle window resize to rearrange grid."""
        super().resizeEvent(event)
        self.image_grid.update_grid(self.width())