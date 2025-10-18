from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout

from utils.ImageUtils import collect_images
from utils.SearchUtil import index_images
from widgets.ImageGrid import ImageGrid
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


        self.scroll_area = QScrollArea()
        self.image_grid = ImageGrid(collect_images(self.folder_path))
        self.scroll_area.setWidget(self.image_grid)

        window_layout = QVBoxLayout()
        window_layout.addWidget(top_row)
        window_layout.addWidget(self.scroll_area)

        self.setLayout(window_layout)

    def on_search(self, search_term):
        image_paths = []
        for entry in self.index:
            for token in entry["tokens"]:
                if search_term.lower() in token:
                    image_paths.append(entry["path"])
                    break


        # self.layout().removeWidget(self.image_grid)
        self.image_grid = ImageGrid(image_paths)
        self.scroll_area.setWidget(self.image_grid)

        # self.layout().addWidget(self.image_grid)

    def resizeEvent(self, event):
        """Handle window resize to rearrange grid."""
        super().resizeEvent(event)
        self.image_grid.update_grid(self.width())