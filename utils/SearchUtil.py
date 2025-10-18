import json
import os
import re

from utils.ImageUtils import collect_images

index_filename = ".search-index"

def index_images(root_dir):
    file_path = os.path.join(root_dir, index_filename)
    if os.path.exists(file_path):
        with open(file_path, "r") as index_file:
            return json.load(index_file)

    image_list = collect_images(root_dir)
    image_data = []

    for image_path in image_list:
        tokens = extract_filename_tokens(image_path)
        image_data.append({ "path": image_path, "tokens": tokens  })

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