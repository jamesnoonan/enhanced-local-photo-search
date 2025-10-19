import json
import os
import re

from utils.ImageCaptioning import ImageCaptioner
from utils.ImageUtils import collect_images, thumbnail_dir_name, get_original_image_path
from widgets.ProgressDialog import show_progress_dialog

index_filename = ".search-index"

def index_images(folder_path):
    file_path = os.path.join(folder_path, index_filename)
    if os.path.exists(file_path):
        with open(file_path, "r") as index_file:
            return json.load(index_file)

    thumbnail_path = os.path.join(folder_path, thumbnail_dir_name)

    image_list = collect_images(thumbnail_path)
    image_data = []

    progress = show_progress_dialog("Creating search index...", len(image_list))
    image_captioner = ImageCaptioner()

    for i, image_path in enumerate(image_list):
        print(f"{i+1} of {len(image_list)} {image_path}")

        filename = os.path.basename(image_path)
        caption = image_captioner.caption(image_path)
        image_data.append({ "path": get_original_image_path(image_path), "filename": filename.lower(), "caption": caption.lower()  })

        progress.setValue(i+1)

    with open(file_path, "w") as index_file:
        json.dump(image_data, index_file)

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