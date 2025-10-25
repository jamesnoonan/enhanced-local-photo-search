from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLabel

from utils.ImageUtils import collect_images, page_size_limit
from utils.SearchUtils import index_images
from widgets.ImageGrid import ImageGrid
from widgets.Pagination import PaginationControls
from widgets.SearchBar import SearchBar

class SearchView(QWidget):
    def __init__(self, folder_path):
        super().__init__()

        self.scroll_area = None
        self.image_grid = None
        self.pagination_controls = None
        self.folder_path = folder_path
        self.index = index_images(folder_path)

        self.images = []
        self.filtered_images = []
        self.page_index = 0
        self.init_ui()

    def init_ui(self):
        top_row = SearchBar(self.on_search, self.folder_path)
        self.images = collect_images(self.folder_path)
        self.filtered_images = self.images

        self.scroll_area = QScrollArea()
        self.update_image_grid()

        window_layout = QVBoxLayout()
        window_layout.setSpacing(0)
        window_layout.addWidget(top_row)
        window_layout.addWidget(self.scroll_area)

        self.setLayout(window_layout)
        self.init_pagination()

    def init_pagination(self):
        layout = self.layout()
        if self.pagination_controls is not None:
            layout.removeWidget(self.pagination_controls)

        self.page_index = 0
        total_page_count = len(self.filtered_images) // page_size_limit + 1

        self.pagination_controls = PaginationControls(total_page_count)
        self.pagination_controls.page_changed.connect(self.change_page)

        layout.addWidget(self.pagination_controls)

    def update_image_grid(self):
        self.image_grid = ImageGrid(self.folder_path, self.images, self.page_index)
        self.scroll_area.setWidget(self.image_grid)

        self.update()

    def change_page(self, page_index):
        self.page_index = page_index
        self.update_image_grid()

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

        self.filtered_images = image_paths
        self.init_pagination()

        self.image_grid = ImageGrid(self.folder_path, image_paths, self.page_index)
        self.scroll_area.setWidget(self.image_grid)