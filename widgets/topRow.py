from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget


class TopRow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        search_box_line_edit = QLineEdit()
        search_button = QPushButton("Search")

        # Header Row
        header_row = QHBoxLayout()
        header_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_row.addWidget(search_box_line_edit)
        header_row.addWidget(search_button)

        self.setLayout(header_row)