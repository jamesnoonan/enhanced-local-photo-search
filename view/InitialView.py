from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout

from utils.ImageUtils import open_folder
from widgets.Spinner import Spinner


class InitialView(QWidget):
    def __init__(self, callback):
        super().__init__()

        self.callback = callback
        self.column = QVBoxLayout()

        self.init_ui()

    def init_ui(self):
        self.column.setAlignment(Qt.AlignmentFlag.AlignCenter)

        app_title = QLabel("<h1>Enhanced Local Photo Search</h1>")
        app_subtitle = QLabel("Open a folder to start")

        select_folder_button: QPushButton = QPushButton("Select Folder", self)
        select_folder_button.clicked.connect(self.select_folder)

        self.column.addWidget(app_title)
        self.column.addWidget(app_subtitle)
        self.column.addWidget(select_folder_button)
        self.setLayout(self.column)

    def select_folder(self):
        row = QHBoxLayout()
        row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        loading_spinner = Spinner()
        row.addWidget(loading_spinner)

        self.column.addLayout(row)

        try:
            folder_path = open_folder("Choose source folder")
            self.callback(folder_path)
        except Exception as e:
            print(e)
            return row.removeWidget(loading_spinner)
