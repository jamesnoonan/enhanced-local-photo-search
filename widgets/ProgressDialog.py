from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QProgressDialog


def show_progress_dialog(title, total_iterations):
    progress = QProgressDialog(title, "Cancel", 0, total_iterations)
    progress.setWindowModality(Qt.WindowModality.ApplicationModal)
    progress.setMinimumDuration(0)  # Show immediately
    progress.setValue(0)
    progress.setMinimumWidth(500)

    return progress