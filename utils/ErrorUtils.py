from PyQt6.QtWidgets import QMessageBox


def show_error(message):
    dialog = QMessageBox()
    dialog.setWindowTitle("Error!")
    dialog.setText(message)
    dialog.exec()