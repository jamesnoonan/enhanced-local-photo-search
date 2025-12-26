import os

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

    return os.path.normpath(original_path)