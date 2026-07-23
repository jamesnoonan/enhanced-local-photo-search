import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout

from utils.ErrorUtils import show_error
from utils.ImageUtils import open_folder
from utils.SearchUtils import does_search_index_exist
from utils.ThumbnailWorker import run_thumbnail_worker
from widgets.ProgressBar import ProgressBar
from widgets.Spinner import Spinner


class InitialView(QWidget):
    def __init__(self, callback):
        super().__init__()

        self.callback = callback
        self.column = QVBoxLayout()
        self.column.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.column.setSpacing(2)

        self.progress_bar = ProgressBar("Creating thumbnails...", "Please wait")
        self.init_selection_ui()

    def init_selection_ui(self):
        clear_layout(self.column)

        app_title = QLabel("<h1>Enhanced Local Photo Search</h1>")

        full_select_folder_label = QLabel("Open a folder and update cache")
        select_folder_button: QPushButton = QPushButton("Load Folder", self)
        select_folder_button.clicked.connect(self.select_folder)

        quick_select_folder_label = QLabel("Open a folder without checking for updates")
        quick_select_folder_button: QPushButton = QPushButton("Quick Load Folder", self)
        quick_select_folder_button.clicked.connect(lambda: self.select_folder(True))

        self.column.addWidget(app_title)
        self.column.addSpacing(25)

        self.column.addWidget(select_folder_button)
        self.column.addWidget(full_select_folder_label)
        self.column.addSpacing(20)

        self.column.addWidget(quick_select_folder_button)
        self.column.addWidget(quick_select_folder_label)
        self.column.addSpacing(20)

        self.setLayout(self.column)

    def init_indexing_ui(self):
        clear_layout(self.column)

        self.column.addWidget(self.progress_bar)
        self.column.addSpacing(10)
        self.column.addWidget(Spinner(), alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(self.column)

    def select_folder(self, quick_load=False):
        row = QHBoxLayout()
        row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        loading_spinner = Spinner()
        row.addWidget(loading_spinner)

        self.column.addLayout(row)

        try:
            folder_path = open_folder("Choose source folder")
            self.init_indexing_ui()
            self.create_thumbnails(folder_path, quick_load)
        except Exception as e:
            print(e)
            return row.removeWidget(loading_spinner)

    def create_thumbnails(self, folder_path: str, quick_load: bool):
        search_index_exists = does_search_index_exist(folder_path)

        try:
            if (not search_index_exists) or (not quick_load):
                run_thumbnail_worker(
                    folder_path,
                    self,
                    lambda x: self.progress_bar.set_progress(x.progress, x.total),
                    lambda: self.callback(folder_path, quick_load)
                )
            else:
                self.callback(folder_path, quick_load)

        except Exception as error:
            print(error)
            show_error("An error occurred: " + str(error))
            sys.exit(1)

def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
        elif item.layout():
            clear_layout(item.layout())
