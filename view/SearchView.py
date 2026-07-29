import shutil
from typing import Optional

from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QApplication, QProgressDialog

from data.SearchQuery import SearchQuery
from utils.ErrorUtils import show_error
from utils.ImageUtils import collect_images, page_size_limit, open_folder, open_file, collect_thumbnails
from utils.IndexWorker import run_index_worker
from utils.PathUtils import get_original_image_path
from utils.SearchUtils import does_search_index_exist
from widgets.ImageGrid import ImageGrid
from widgets.Pagination import PaginationControls
from widgets.ProgressBar import ProgressBar
from widgets.ProgressDialog import show_progress_dialog
from widgets.SearchBar import SearchBar, file_filter_all_value

# The minimum size of the results in order to show a loading bar when searching
show_progress_limit = 100

class SearchView(QWidget):
    def __init__(self, folder_path, quick_load: bool):
        super().__init__()

        self.quick_load = quick_load

        self.scroll_area = None
        self.image_grid = None
        self.pagination_controls = None

        self.folder_path = folder_path
        self.index = None

        self.window_layout = QVBoxLayout()
        self.progress_bar = ProgressBar("Processing search results", "Loading model...")

        run_index_worker(folder_path, quick_load, self, self.on_index_progress, self.on_index_finish)

        self.images = []
        self.filtered_images = []
        self.page_index = 0

        self.init_ui()

    def init_ui(self):
        self.scroll_area = QScrollArea()

        self.window_layout.setSpacing(0)
        self.window_layout.addWidget(self.progress_bar)
        self.window_layout.addWidget(self.scroll_area)

        self.setLayout(self.window_layout)
        self.update_results(self.images)

    def on_search(self, search_query: SearchQuery):
        if self.index is None:
            show_error("Please wait until the index finishes processing")
            return

        if search_query.search_filenames or search_query.search_ai_data:
            empty_query = len(search_query.query_terms) == 0
            no_file_type_filter = search_query.file_type_filter == file_filter_all_value

            if empty_query and no_file_type_filter:
                self.update_results(self.get_all_images_from_index())
            else:
                self.update_results(self.run_search(search_query))
        else:
            self.update_results([])

    def run_search(self, search_query: SearchQuery):
        image_paths = []
        progress: QProgressDialog | None = None
        if len(self.index) > show_progress_limit:
            progress = show_progress_dialog("Searching images...", len(self.index))

        for i, entry in enumerate(self.index):
            filename = entry["filename"]
            caption = entry["caption"]
            extension = "." + (entry["path"].split(".")[-1]).lower()

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

        return image_paths

    def on_export(self):
        progress: Optional[QProgressDialog] = None

        try:
            export_folder_path = open_folder("Choose folder to copy to")

            progress: QProgressDialog = show_progress_dialog("Copying images...", len(self.filtered_images))
            for i, image_path in enumerate(self.filtered_images):
                shutil.copy(image_path, export_folder_path)
                progress.setValue(i + 1)
                QApplication.processEvents()
            progress.close()

            open_file(export_folder_path)
        except AssertionError:
            print("Info: Export operation cancelled")
        except FileNotFoundError:
            print("Error: Could not find one or more images")
            if progress is not None:
                progress.close()
            show_error("The program could not find one or more images from the search results! You may be missing the original image")
        except Exception as e:
            if progress is not None:
                progress.close()
            print("Error: unexpected error:", e)
            show_error(f"Failed to copy images to folder (image may already exist)")

    def on_change_page(self, page_index):
        self.page_index = page_index
        self.update_image_grid()

    def resizeEvent(self, event: QResizeEvent | None) -> None:
        self.update_image_grid()
        super().resizeEvent(event)

    def get_all_images_from_index(self):
        return list(map(lambda image: image["path"], self.index))

    def update_results(self, results):
        self.filtered_images = results
        self.update_pagination()
        self.update_image_grid()

    def update_pagination(self):
        layout = self.window_layout
        if self.pagination_controls is not None:
            layout.removeWidget(self.pagination_controls)

        self.page_index = 0
        total_page_count = len(self.filtered_images) // page_size_limit + 1

        self.pagination_controls = PaginationControls(total_page_count)
        self.pagination_controls.page_changed.connect(self.on_change_page)

        layout.addWidget(self.pagination_controls)

    def update_image_grid(self):
        self.image_grid = ImageGrid(self.folder_path, self.filtered_images, self.page_index, self.width())
        self.scroll_area.setWidget(self.image_grid)

        self.update()

    def on_index_progress(self, progress):
        self.progress_bar.set_subtitle("Indexing results...")
        self.progress_bar.set_progress(progress.progress, progress.total)

    def on_index_finish(self, index):
        self.index = index
        self.images = self.get_all_images_from_index()
        self.update_results(self.images)

        # Remove progress bar
        self.window_layout.removeWidget(self.progress_bar)
        self.progress_bar.deleteLater()

        # Add search box
        top_row = SearchBar(self.on_search, self.on_export, self.folder_path)
        no_search_index = not does_search_index_exist(self.folder_path)

        if not (self.quick_load and no_search_index):
            self.window_layout.insertWidget(0, top_row)
