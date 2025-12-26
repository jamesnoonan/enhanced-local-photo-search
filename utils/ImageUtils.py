import os
import subprocess
import sys

from PIL import Image
from PyQt6.QtWidgets import QFileDialog

from utils.ErrorUtils import show_error
from utils.PathUtils import get_thumbnail_path
from widgets.ProgressDialog import show_progress_dialog

page_size_limit = 120
thumbnail_dir_name = ".thumbnails"
image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp', '.tif', '.tiff')

def is_image_file(filename):
    return os.path.splitext(filename.lower())[1] in image_extensions

def collect_images(directory_path):
    image_list: list[str] = []
    for root, dirs, files in os.walk(directory_path):
        if thumbnail_dir_name in dirs:
            dirs.remove(thumbnail_dir_name) # Skip .thumbnails directories to prevent nesting

        for file in files:
            if is_image_file(file):
                full_path = os.path.join(root, file)
                image_list.append(os.path.normpath(full_path))
    return sorted(image_list, key=lambda path: os.path.basename(path).lower())

def collect_thumbnails(directory_path):
    return collect_images(os.path.join(directory_path, thumbnail_dir_name))

def open_folder(text="Select Folder"):
    folder_path = QFileDialog.getExistingDirectory(None, text)
    if not folder_path:
       raise AssertionError("Folder not found")

    return folder_path


def open_image(root_dir, image_path):
    if os.path.exists(image_path) and os.path.isfile(image_path):
        open_file(image_path)
        return

    thumbnail_path = get_thumbnail_path(root_dir, image_path)
    if thumbnail_path:
        if os.path.exists(thumbnail_path) and os.path.isfile(thumbnail_path):
            open_file(thumbnail_path)
            return

    show_error(f"Could not open {image_path} or its thumbnail.")


def open_file(file_path):
    try:
        if sys.platform == "win32":
            os.startfile(file_path)  # Windows
        elif sys.platform == "darwin":
            subprocess.run(["open", file_path])  # macOS
        else:
            subprocess.run(["xdg-open", file_path])  # Linux
    except FileNotFoundError:
        show_error(f"Error: Image file not found at '{file_path}'.")
    except Exception as e:
        show_error(f"An error occurred: {e}")

def create_thumbnails(root_dir, thumbnail_size=(256, 256)):
    all_images = collect_images(root_dir)

    progress = show_progress_dialog("Creating thumbnails...", len(all_images))

    thumb_dir = os.path.join(root_dir, ".thumbnails")
    os.makedirs(thumb_dir, exist_ok=True)

    for img_index, img_path in enumerate(all_images):
        if progress.wasCanceled():
            print("Thumbnail creation canceled by user")
            break

        thumb_path = get_thumbnail_path(root_dir, img_path)
        if os.path.exists(thumb_path):
            progress.setValue(img_index + 1)
            continue  # Skip if thumbnail already exists

        os.makedirs(os.path.dirname(thumb_path), exist_ok=True)

        try:
            with Image.open(img_path) as img:
                if img.mode not in ("RGB", "L"):
                    if img.mode == "I;16":
                        img = img.point(lambda i: i * (1. / 256)).convert("L")
                    else:
                        img = img.convert("RGB")

                img.thumbnail(thumbnail_size)
                img.save(thumb_path, "JPEG")
                print(f"Thumbnail created: {thumb_path}")

        except Exception as e:
            print(f"Failed to create thumbnail for {img_path}: {e}")

        progress.setValue(img_index + 1)

    progress.close()