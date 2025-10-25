import json
import os
import re
import shutil
import sys

from utils.ImageCaptioning import ImageCaptioner
from utils.ImageUtils import collect_images, thumbnail_dir_name, get_original_image_path, get_thumbnail_path
from widgets.ProgressDialog import show_progress_dialog

index_filename = ".search-index"

def index_images(folder_path):
    image_data = []

    file_path = os.path.join(folder_path, index_filename)
    if os.path.exists(file_path):
        with open(file_path, "r") as index_file:
            image_data = json.load(index_file)

    thumbnail_folder_path = os.path.join(folder_path, thumbnail_dir_name)
    thumbnail_paths = collect_images(thumbnail_folder_path)

    progress = show_progress_dialog("Loading search index...", len(image_data))
    # Remove images that already appear in the list
    for i, entry in enumerate(image_data):
        stored_path = entry["path"]
        thumbnail_paths.remove(get_thumbnail_path(folder_path, stored_path))

        progress.setValue(i + 1)
    progress.close()

    # Exit early if no new files
    if len(thumbnail_paths) == 0:
        return image_data

    image_captioner = ImageCaptioner()

    progress = show_progress_dialog("Creating search index...", len(thumbnail_paths))
    for i, image_path in enumerate(thumbnail_paths):
        print(f"{i+1} of {len(thumbnail_paths)} {image_path}")

        filename = os.path.basename(image_path)
        caption = image_captioner.caption(image_path)
        image_data.append({ "path": get_original_image_path(image_path), "filename": filename.lower(), "caption": caption.lower()  })

        progress.setValue(i+1)

    with open(file_path, "w") as index_file:
        json.dump(image_data, index_file)

    progress.close()
    return image_data


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