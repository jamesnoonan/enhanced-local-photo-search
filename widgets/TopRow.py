from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget


class TopRow(QWidget):
    def __init__(self, on_search):
        super().__init__()
        self.search_box_line_edit = None
        self.search_callback = on_search
        self.init_ui()


    def init_ui(self):
        self.search_box_line_edit: QLineEdit = QLineEdit()
        self.search_box_line_edit.setPlaceholderText("Type search terms here..")
        self.search_box_line_edit.returnPressed.connect(self.on_search)

        search_button: QPushButton = QPushButton("Search")
        search_button.clicked.connect(self.on_search)

        header_row = QHBoxLayout()
        header_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_row.addWidget(self.search_box_line_edit)
        header_row.addWidget(search_button)

        self.setLayout(header_row)

    def on_search(self):
        self.search_callback(self.search_box_line_edit.text())

    def on_key_press(self, event):
        if event.key() == Qt.Key.Key_Enter:
            self.on_search()