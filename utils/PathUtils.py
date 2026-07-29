import os
from pathlib import Path


def get_thumbnail_path(root_path: str, img_path: str):
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

def get_original_image_path(thumbnail_path: str):
    p = Path(thumbnail_path)
    parts = list(p.parts)

    # Remove the first occurrence of ".thumbnails"
    try:
        thumb_index = parts.index(".thumbnails")
    except ValueError:
        raise ValueError(f"Expected '.thumbnails' directory in path: {thumbnail_path}")

    # Rebuild path without the ".thumbnails" directory
    original_parts = parts[:thumb_index] + parts[thumb_index + 1:]
    thumb_filename = original_parts.pop()

    # Extract original filename
    name, _ = os.path.splitext(thumb_filename)
    if "_" not in name:
        raise ValueError(f"Thumbnail filename does not follow expected format: {thumb_filename}")

    base_name, original_ext = name.rsplit("_", 1)
    original_filename = f"{base_name}.{original_ext}"
    original_parts.append(original_filename)

    return os.path.normpath(os.path.join(*original_parts))