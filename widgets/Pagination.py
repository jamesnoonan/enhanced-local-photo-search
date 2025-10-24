from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLabel
)

class PaginationControls(QWidget):
    page_changed: pyqtSignal = pyqtSignal(int)  # emits the new page number

    def __init__(self, total_pages=1):
        super().__init__()
        self.current_page = 0
        self.total_pages = total_pages

        # --- Layout ---
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # --- Buttons ---
        self.prev_btn: QPushButton = QPushButton("◀ Prev")
        self.next_btn: QPushButton = QPushButton("Next ▶")
        self.page_label = QLabel()
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)

        layout.addWidget(self.prev_btn)
        layout.addWidget(self.page_label)
        layout.addWidget(self.next_btn)

        self.update_ui()

    def update_ui(self):
        self.page_label.setText(f"Page {self.current_page + 1} / {self.total_pages}")
        self.prev_btn.setEnabled(self.current_page > 0)
        self.next_btn.setEnabled(self.current_page < self.total_pages - 1)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_ui()
            self.on_page_change()

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_ui()
            self.on_page_change()

    def on_page_change(self):
         self.page_changed.emit(self.current_page)


