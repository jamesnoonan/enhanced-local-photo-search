from PyQt6.QtCore import QObject, pyqtSignal, QThread

from utils.ImageUtils import create_thumbnails


def run_thumbnail_worker(folder_path: str, parent, progress_callback, finished_callback):
    parent.thread = QThread(parent)
    parent.worker = ThumbnailWorker(folder_path)

    parent.worker.moveToThread(parent.thread)

    parent.thread.started.connect(parent.worker.run)
    parent.worker.progress.connect(progress_callback)
    parent.worker.finished.connect(finished_callback)

    # Cleanup
    parent.worker.finished.connect(parent.thread.quit)
    parent.worker.finished.connect(parent.worker.deleteLater)
    parent.thread.finished.connect(parent.thread.deleteLater)

    parent.thread.start()

class ThumbnailProgress:
    def __init__(self, progress, total):
        self.progress = progress
        self.total = total

class ThumbnailWorker(QObject):
    progress = pyqtSignal(object)
    finished = pyqtSignal()

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path

    def update_progress(self, done, total):
        progress_object = ThumbnailProgress(done, total)
        self.progress.emit(progress_object)

    def run(self):
        create_thumbnails(self.folder_path, self.update_progress)
        self.finished.emit()
