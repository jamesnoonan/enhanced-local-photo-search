import json
import os
import re
import shutil
import sys

from PyQt6.QtWidgets import QMessageBox

from utils.ImageUtils import thumbnail_dir_name

index_filename: str = ".search-index"

def get_search_index_path(folder_path):
    return os.path.join(folder_path, index_filename)

def does_search_index_exist(folder_path):
    return os.path.exists(get_search_index_path(folder_path))

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