from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QComboBox, QCheckBox, QSizePolicy

from data.SearchQuery import SearchQuery
from utils.ImageUtils import image_extensions
from utils.SearchUtils import clear_cache

file_filter_all_value = "All file types"

class SearchBar(QWidget):
    def __init__(self, on_search, on_export, folder_path):
        super().__init__()
        self.search_box_line_edit = None
        self.use_filename_checkbox = None
        self.use_ai_data_checkbox = None
        self.file_type_filter = None

        self.search_callback = on_search
        self.on_export = on_export
        self.folder_path = folder_path
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

        # File type dropdown
        self.file_type_filter: QComboBox = QComboBox()
        self.file_type_filter.addItem(file_filter_all_value)
        self.file_type_filter.addItems(image_extensions)
        self.file_type_filter.currentTextChanged.connect(self.on_search)

        # Checkboxes
        checkbox_row_widget = QWidget()
        checkbox_row = QHBoxLayout(checkbox_row_widget)
        checkbox_row.setContentsMargins(0, 0, 0, 0)

        self.use_filename_checkbox: QCheckBox = QCheckBox("Search filename")
        self.use_filename_checkbox.setChecked(True)
        self.use_filename_checkbox.checkStateChanged.connect(self.on_search)

        self.use_ai_data_checkbox: QCheckBox = QCheckBox("Search AI caption")
        self.use_ai_data_checkbox.setChecked(True)
        self.use_ai_data_checkbox.checkStateChanged.connect(self.on_search)

        checkbox_row.addWidget(self.use_filename_checkbox)
        checkbox_row.addWidget(self.use_ai_data_checkbox)
        checkbox_row_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        checkbox_row_widget.adjustSize()

        # Buttons
        export_button: QPushButton = QPushButton("Copy results to folder")
        export_button.clicked.connect(self.on_export)

        clear_button: QPushButton = QPushButton("Clear cache and exit")
        clear_button.clicked.connect(self.on_clear_cache)

        # Add all to row
        filter_row.addWidget(checkbox_row_widget)
        filter_row.addWidget(self.file_type_filter)
        filter_row.addWidget(export_button)
        filter_row.addWidget(clear_button)

        return filter_row

    def on_search(self):
        query = self.search_box_line_edit.text()
        search_filenames = self.use_filename_checkbox.isChecked()
        search_ai_data = self.use_ai_data_checkbox.isChecked()

        file_type_filter = self.file_type_filter.currentText()
        file_type_filter = None if file_type_filter == file_filter_all_value else file_type_filter

        search_query = SearchQuery(query, file_type_filter, search_filenames, search_ai_data)
        self.search_callback(search_query)

    def on_clear_cache(self):
        clear_cache(self.folder_path)

    def on_key_press(self, event):
        if event.key() == Qt.Key.Key_Enter:
            self.on_search()
