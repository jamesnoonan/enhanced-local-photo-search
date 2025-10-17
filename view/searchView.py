from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout

from imageUtils import open_folder
from widgets.imageGrid import ImageGrid
from widgets.topRow import TopRow

class SearchView(QWidget):
    def __init__(self, folder_path):
        super().__init__()

        self.folder_path = folder_path
        self.init_ui()

    def init_ui(self):
        top_row = TopRow()
        image_grid = ImageGrid(self.folder_path)

        scroll_area = QScrollArea()
        scroll_area.setWidget(image_grid)

        window_layout = QVBoxLayout()
        window_layout.addWidget(top_row)
        window_layout.addWidget(scroll_area)

        self.setLayout(window_layout)