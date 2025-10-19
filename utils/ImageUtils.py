import os
import subprocess
import sys

from PIL import Image
from PyQt6.QtWidgets import QFileDialog

from widgets.ProgressDialog import show_progress_dialog

thumbnail_dir_name = ".thumbnails"
image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp', '.tif', '.tiff')

def is_image_file(filename):
    return os.path.splitext(filename.lower())[1] in image_extensions

def collect_images(directory_path):
    image_list = []
    for root, dirs, files in os.walk(directory_path):
        if thumbnail_dir_name in dirs:
            dirs.remove(thumbnail_dir_name) # Skip .thumbnails directories to prevent nesting

        for file in files:
            if is_image_file(file):
                full_path = os.path.join(root, file)
                image_list.append(full_path)
    return image_list

def open_folder():
    folder_path = QFileDialog.getExistingDirectory(None, "Select Image Folder")
    if not folder_path:
       raise Exception("Folder not found")

    return folder_path


def get_original_image_path(thumbnail_path):
    parts = thumbnail_path.split(os.sep)

    # Keep track if path was absolute
    is_absolute = thumbnail_path.startswith(os.sep)

    # Remove the first occurrence of ".thumbnails"
    try:
        thumb_index = parts.index(".thumbnails")
    except ValueError:
        raise ValueError(f"Expected '.thumbnails' directory in path: {thumbnail_path}")

    # Rebuild path without the ".thumbnails" directory
    original_parts = parts[:thumb_index] + parts[thumb_index + 1:]
    original_dir, thumb_filename = os.path.split(os.path.join(*original_parts))

    # Extract original filename
    name, _ = os.path.splitext(thumb_filename)
    if "_" not in name:
        raise ValueError(f"Thumbnail filename does not follow expected format: {thumb_filename}")

    base_name, orig_ext = name.rsplit("_", 1)
    original_filename = f"{base_name}.{orig_ext}"

    original_path = os.path.join(original_dir, original_filename)

    # Prepend leading slash if the original thumbnail path was absolute
    if is_absolute and not original_path.startswith(os.sep):
        original_path = os.sep + original_path

    return original_path


def open_image(image_path):
    try:
        if sys.platform == "win32":
            os.startfile(image_path)  # Windows
        elif sys.platform == "darwin":
            subprocess.run(["open", image_path])  # macOS
        else:
            subprocess.run(["xdg-open", image_path])  # Linux
    except FileNotFoundError:
        print(f"Error: Image file not found at '{image_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_thumbnail_path(root_path, img_path):
    """
    Return the thumbnail path under root_path/.thumbnails, preserving subfolders.
    Works with absolute or relative img_path.
    """
    # Make image path relative to root_path
    rel_path = os.path.relpath(img_path, root_path)  # e.g., "EHS-0016 ... .tif"
    dirpath, filename = os.path.split(rel_path)
    name, ext = os.path.splitext(filename)
    ext_clean = ext.lower().lstrip('.')  # "tif"

    # Thumbnail directory inside root_path/.thumbnails, preserving subfolders
    thumb_dir = os.path.join(root_path, ".thumbnails", dirpath)

    # Thumbnail filename
    thumb_filename = f"{name}_{ext_clean}.jpg"

    # Full thumbnail path
    thumb_path = os.path.join(thumb_dir, thumb_filename)
    return os.path.normpath(thumb_path)

def create_thumbnails(root_dir, thumbnail_size=(256, 256)):
    all_images = collect_images(root_dir)

    progress = show_progress_dialog("Creating thumbnails...", len(all_images))

    thumb_dir = os.path.join(root_dir, ".thumbnails")
    os.makedirs(thumb_dir, exist_ok=True)

    for i, img_path in enumerate(all_images):
        if progress.wasCanceled():
            print("Thumbnail creation canceled by user")
            break

        thumb_path = get_thumbnail_path(root_dir, img_path)
        if os.path.exists(thumb_path):
            progress.setValue(i + 1)
            continue  # Skip if thumbnail already exists

        os.makedirs(os.path.dirname(thumb_path), exist_ok=True)

        try:
            with Image.open(img_path) as img:
                img.thumbnail(thumbnail_size)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.save(thumb_path, "JPEG")
                print(f"Thumbnail created: {thumb_path}")
        except Exception as e:
            print(f"Failed to create thumbnail for {img_path}: {e}")

        progress.setValue(i + 1)

    progress.close()