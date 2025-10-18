import os
import subprocess
import sys

from PIL import Image
from PyQt6.QtWidgets import QFileDialog

image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp', '.tif', '.tiff')

def is_image_file(filename):
    return os.path.splitext(filename.lower())[1] in image_extensions

def collect_images(directory_path):
    image_list = []
    for root, dirs, files in os.walk(directory_path):
        if '.thumbnails' in dirs:
            dirs.remove('.thumbnails') # Skip .thumbnails directories to prevent nesting

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

def open_image(image_path):
    parts = image_path.split(os.sep)
    if ".thumbnails" in parts:
        idx = parts.index(".thumbnails")
        # Reconstruct path without the '.thumbnails' part
        new_path = os.sep.join(parts[:idx] + parts[idx + 1:])
        if os.path.exists(new_path):
            image_path = new_path
            print(f"Redirected to original image: {image_path}")
        else:
            print(f"Original image not found at '{new_path}', using thumbnail path.")

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

def create_thumbnails(root_dir, thumbnail_size=(256, 256)):
    all_images = collect_images(root_dir)

    for img_path in all_images:
        dirpath, filename = os.path.split(img_path)
        thumb_dir = os.path.join(dirpath, ".thumbnails")
        os.makedirs(thumb_dir, exist_ok=True)

        thumb_path = os.path.join(thumb_dir, filename)

        if os.path.exists(thumb_path):
            continue  # Skip if thumbnail already exists

        try:
            with Image.open(img_path) as img:
                img.thumbnail(thumbnail_size)
                img.save(thumb_path)
                print(f"Thumbnail created: {thumb_path}")
        except Exception as e:
            print(f"Failed to create thumbnail for {img_path}: {e}")

