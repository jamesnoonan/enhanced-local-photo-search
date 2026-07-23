import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from utils.ErrorUtils import show_error
from utils.ThumbnailWorker import run_thumbnail_worker
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

    def open_folder(self, folder_path, quick_load: bool):
        try:
            if not quick_load:
                run_thumbnail_worker(folder_path, self, lambda x: print(x.progress), lambda: self.show_results_screen(folder_path, quick_load))
            else:
                self.show_results_screen(folder_path, quick_load)

        except Exception as error:
            print(error)
            show_error("An error occurred: " + str(error))
            sys.exit(1)

    def show_results_screen(self, folder_path: str, quick_load: bool):
        if not self.search_view:
            self.search_view = SearchView(folder_path, quick_load)
            self.stack.addWidget(self.search_view)

        self.stack.setCurrentWidget(self.search_view)

if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QIcon("icon.png"))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
