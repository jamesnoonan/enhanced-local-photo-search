from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QComboBox, QCheckBox, QSizePolicy

from utils.ImageUtils import image_extensions

class SearchBar(QWidget):
    def __init__(self, on_search):
        super().__init__()
        self.search_box_line_edit = None
        self.search_callback = on_search
        self.init_ui()

    def init_ui(self):
        header_row = self.init_header_row()
        filter_row = self.init_filter_row()

        search_bar_layout = QVBoxLayout()
        search_bar_layout.addLayout(header_row)
        search_bar_layout.addLayout(filter_row)

        self.setLayout(search_bar_layout)

    def init_header_row(self):
        # Text field for search terms
        search_box_line_edit: QLineEdit = QLineEdit()
        search_box_line_edit.setStyleSheet("padding: 5px")
        search_box_line_edit.setPlaceholderText("Type search terms here...")
        search_box_line_edit.returnPressed.connect(self.on_search)
        self.search_box_line_edit = search_box_line_edit

        # Button to search
        search_button: QPushButton = QPushButton("Search")
        search_button.clicked.connect(self.on_search)

        header_row = QHBoxLayout()
        header_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_row.addWidget(self.search_box_line_edit)
        header_row.addWidget(search_button)

        return header_row

    def init_filter_row(self):
        filter_row = QHBoxLayout()

        file_type_filter = QComboBox()
        file_type_filter.addItem("All file types")
        file_type_filter.addItems(image_extensions)

        export_button: QPushButton = QPushButton("Copy results to folder")


        clear_button: QPushButton = QPushButton("Clear cache and exit")
        clear_button.clicked.connect(self.on_clear)

        checkbox_row_widget = QWidget()
        checkbox_row = QHBoxLayout(checkbox_row_widget)
        checkbox_row.setContentsMargins(0, 0, 0, 0)

        use_filename_checkbox = QCheckBox("Search filename")
        use_ai_caption_checkbox = QCheckBox("Search AI caption")
        use_filename_checkbox.setChecked(True)
        use_ai_caption_checkbox.setChecked(True)

        checkbox_row.addWidget(use_filename_checkbox)
        checkbox_row.addWidget(use_ai_caption_checkbox)
        checkbox_row_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        checkbox_row_widget.adjustSize()

        filter_row.addWidget(checkbox_row_widget)
        filter_row.addWidget(file_type_filter)
        filter_row.addWidget(export_button)
        filter_row.addWidget(clear_button)

        return filter_row

    def on_search(self):
        self.search_callback(self.search_box_line_edit.text())

    def on_clear(self):
        pass

    def on_key_press(self, event):
        if event.key() == Qt.Key.Key_Enter:
            self.on_search()