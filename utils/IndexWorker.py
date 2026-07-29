import json
import os

from utils.ImageCaptioner import ImageCaptioner
from utils.ImageUtils import thumbnail_dir_name, collect_images
from utils.PathUtils import get_thumbnail_path, get_original_image_path
from utils.SearchUtils import get_search_index_path, convert_index_to_absolute
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
        index = self.index_images()
        self.finished.emit(index)

    def index_images(self):
        folder_path = self.folder_path
        quick_load = self.quick_load
        progress_callback = self.update_progress

        image_data = []

        file_path = get_search_index_path(folder_path)
        if os.path.exists(file_path):
            with open(file_path, "r") as index_file:
                image_data = json.load(index_file)
                if quick_load:
                    return convert_index_to_absolute(folder_path, image_data)
        elif quick_load:
            return []

        thumbnail_folder_path = os.path.join(folder_path, thumbnail_dir_name)
        thumbnail_paths = collect_images(thumbnail_folder_path)

        # Remove images that already appear in the list
        for i, entry in enumerate(image_data):
            stored_path = os.path.join(folder_path, entry["path"])
            thumbnail_path = get_thumbnail_path(folder_path, stored_path)

            if thumbnail_path in thumbnail_paths:
                thumbnail_paths.remove(thumbnail_path)


        # Exit early if no new files
        if len(thumbnail_paths) == 0:
            return convert_index_to_absolute(folder_path, image_data)

        image_captioner = ImageCaptioner()
        total_to_index = len(thumbnail_paths)
        progress_callback(0, total_to_index)

        for i, image_path in enumerate(thumbnail_paths):
            print(f"{i+1} of {len(thumbnail_paths)} {image_path}")

            filename = os.path.basename(image_path)
            caption = image_captioner.caption(image_path)
            absolute_path = get_original_image_path(image_path)
            relative_path = os.path.relpath(absolute_path, start=folder_path)
            image_data.append({ "path": relative_path, "filename": filename.lower(), "caption": caption.lower()  })

            progress_callback(i+1, total_to_index)

        # Write results to index file
        with open(file_path, "w") as index_file:
            json.dump(image_data, index_file)

        return convert_index_to_absolute(folder_path, image_data)


