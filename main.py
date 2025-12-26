import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from utils.ErrorUtils import show_error
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
        self.resize(1000, 700)
        self.setMinimumWidth(800)
        self.setMinimumHeight(400)

        self.stack.addWidget(self.initial_view)
        self.setCentralWidget(self.stack)

    def open_folder(self, folder_path):
        try:
            create_thumbnails(folder_path)

            if not self.search_view:
                self.search_view = SearchView(folder_path)
                self.stack.addWidget(self.search_view)

            self.stack.setCurrentWidget(self.search_view)

        except Exception as error:
            print(error)
            show_error("An error occurred: " + str(error))
            sys.exit(1)

if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QIcon("icon.png"))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
