import shutil

from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout

from data.SearchQuery import SearchQuery
from utils.ErrorUtils import show_error
from utils.ImageUtils import collect_images, page_size_limit, open_folder, open_file
from utils.SearchUtils import index_images
from widgets.ImageGrid import ImageGrid
from widgets.Pagination import PaginationControls
from widgets.ProgressDialog import show_progress_dialog
from widgets.SearchBar import SearchBar, file_filter_all_value

show_progress_limit = 100

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
        top_row = SearchBar(self.on_search, self.on_export, self.folder_path)
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
        self.image_grid = ImageGrid(self.folder_path, self.filtered_images, self.page_index)
        self.scroll_area.setWidget(self.image_grid)

        self.update()

    def change_page(self, page_index):
        self.page_index = page_index
        self.update_image_grid()

    def on_search(self, search_query: SearchQuery):
        image_paths = []

        if search_query.search_filenames or search_query.search_ai_data:
            if len(search_query.query_terms) == 0 and search_query.file_type_filter == file_filter_all_value:
                image_paths = list(map(lambda image: image["path"], self.index))
            else:
                progress = None
                if len(self.index) > show_progress_limit:
                    progress = show_progress_dialog("Searching images...", len(self.index))

                for i, entry in enumerate(self.index):
                    filename = entry["filename"]
                    caption = entry["caption"]
                    extension = "."  + (entry["path"].split(".")[-1]).lower()

                    try:
                        does_match = search_query.does_entry_match_query(filename, caption, extension)
                        if does_match:
                            image_paths.append(entry["path"])
                    except ValueError:
                        show_error("Search query is incorrectly formatted")
                        break

                    if progress is not None:
                        progress.setValue(i + 1)

                if progress is not None:
                    progress.close()

        self.filtered_images = image_paths
        self.init_pagination()
        self.update_image_grid()

    def on_export(self):
        try:
            export_folder_path = open_folder("Choose folder to copy to")

            for image_path in self.filtered_images:
                shutil.copy(image_path, export_folder_path)

            open_file(export_folder_path)
        except FileNotFoundError:
            print("Operation cancelled")
        except Exception as e:
            show_error(f"Failed to copy images to folder ({e})")