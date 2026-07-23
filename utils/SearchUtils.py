import json
import os
import re
import shutil
import sys

from PyQt6.QtWidgets import QMessageBox

from utils.ImageCaptioner import ImageCaptioner
from utils.ImageUtils import collect_images, thumbnail_dir_name, get_thumbnail_path, create_thumbnails
from utils.PathUtils import get_original_image_path

index_filename = ".search-index"

def get_search_index_path(folder_path):
    return os.path.join(folder_path, index_filename)

def does_search_index_exist(folder_path):
    return os.path.exists(get_search_index_path(folder_path))

def index_images(folder_path, quick_load: bool, progress_callback):
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

def convert_index_to_absolute(folder_path, image_data):
    output = []

    for entry in image_data:
        absolute_path = os.path.join(folder_path, entry["path"])
        output.append({ "path": absolute_path, "filename": entry["filename"], "caption": entry["caption"] })

    return output

def load_index(root_dir):
    file_path = os.path.join(root_dir, index_filename)
    if os.path.exists(file_path):
        with open(file_path, "r") as index_file:
            return json.load(index_file)

    raise FileNotFoundError(file_path)


def extract_filename_tokens(file_path):
    # Get the filename without directories
    filename = os.path.basename(file_path)
    # Remove the file extension
    name_without_ext = os.path.splitext(filename)[0]
    # Split into tokens using non-alphanumeric characters as delimiters
    tokens = re.split(r'[^A-Za-z0-9]+', name_without_ext)
    # Remove empty tokens and convert to lowercase
    tokens = [token.lower() for token in tokens if token]
    return tokens

def clear_cache(folder_path):
    button = QMessageBox.question(
        None,
        "Are you sure?",
        "This operation will delete all of the created thumbnails and search index, which may take a long time to regenerate. Are you sure?"
    )
    if button != QMessageBox.StandardButton.Yes:
        return

    # Delete all images in .thumbnails folder
    thumbnail_path = os.path.join(folder_path, thumbnail_dir_name)
    if os.path.exists(thumbnail_path):
        shutil.rmtree(thumbnail_path)

    # Delete search index file
    search_index_path = os.path.join(folder_path, index_filename)
    if os.path.exists(search_index_path):
        os.remove(search_index_path)

    # Close program
    sys.exit(0)