import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from utils.ImageUtils import create_thumbnails
from view.InitialView import InitialView
from view.SearchView import SearchView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initial_view = InitialView(self.open_folder)
        self.stack = QStackedWidget()
        self.search_view = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Enhanced Local Photo Search")
        self.setGeometry(100, 100, 725, 650)

        self.stack.addWidget(self.initial_view)
        self.setCentralWidget(self.stack)

    def open_folder(self, folder_path):
        create_thumbnails(folder_path)

        if not self.search_view:
            self.search_view = SearchView(folder_path + "/.thumbnails")
            self.stack.addWidget(self.search_view)

        self.stack.setCurrentWidget(self.search_view)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())