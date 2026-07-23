from utils.SearchUtils import index_images
from PyQt6.QtCore import QObject, pyqtSignal, QThread

def run_index_worker(folder_path: str, quick_load: bool, parent, progress_callback, finished_callback):
    parent.thread = QThread(parent)
    parent.worker = IndexWorker(folder_path, quick_load)

    parent.worker.moveToThread(parent.thread)

    parent.thread.started.connect(parent.worker.run)
    parent.worker.progress.connect(progress_callback)
    parent.worker.finished.connect(finished_callback)

    # Cleanup
    parent.worker.finished.connect(parent.thread.quit)
    parent.worker.finished.connect(parent.worker.deleteLater)
    parent.thread.finished.connect(parent.thread.deleteLater)

    parent.thread.start()

class IndexProgress:
    def __init__(self, progress, total):
        self.progress = progress
        self.total = total

class IndexWorker(QObject):
    progress = pyqtSignal(object)
    finished = pyqtSignal(object)

    def __init__(self, folder_path, quick_load):
        super().__init__()
        self.folder_path = folder_path
        self.quick_load = quick_load

    def update_progress(self, done, total):
        progress_object = IndexProgress(done, total)
        self.progress.emit(progress_object)

    def run(self):
        index = index_images(self.folder_path, self.quick_load, self.update_progress)
        self.finished.emit(index)
