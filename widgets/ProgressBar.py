from PyQt6.QtWidgets import QLabel, QHBoxLayout, QProgressBar, QVBoxLayout, QWidget


class ProgressBar(QWidget):
    def __init__(self, title: str, subtitle: str, parent=None):
        super().__init__(parent)

        self.title_label = QLabel("<h3>" + title + "</h3>")
        self.subtitle_label = QLabel(subtitle)

        self.percentage_label = QLabel("")
        self.progress_bar = QProgressBar()
        self.item_progress_label = QLabel("")

        row = QHBoxLayout()
        row.addWidget(self.percentage_label)
        row.addWidget(self.progress_bar)
        row.addWidget(self.item_progress_label)

        column = QVBoxLayout()
        column.addWidget(self.title_label)
        column.addWidget(self.subtitle_label)
        column.addLayout(row)

        self.setLayout(column)

    def set_title(self, title: str):
        self.title_label.setText(title)

    def set_subtitle(self, subtitle: str):
        self.subtitle_label.setText(subtitle)

    def set_progress(self, progress: int, total: int):
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(progress)

        percentage = round(progress / total * 100)
        self.percentage_label.setText(str(percentage) + "%")
        self.item_progress_label.setText(str(progress) + " of " + str(total))
