import os
from PIL import Image
from PyQt6.QtWidgets import QFileDialog

def open_folder():
    folder_path = QFileDialog.getExistingDirectory(None, "Select Image Folder")
    if not folder_path:
       raise Exception("Folder not found")

    return folder_path


def create_thumbnails(root_dir, thumbnail_size=(256, 256)):
    """
    Recursively goes through root_dir and creates thumbnails of all image files
    in a .thumbnails subdirectory, but only if a thumbnail doesn't already exist.
    """
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tif', '.tiff')

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip .thumbnails directories to prevent nesting
        if '.thumbnails' in dirnames:
            dirnames.remove('.thumbnails')

        thumb_dir = os.path.join(dirpath, ".thumbnails")
        os.makedirs(thumb_dir, exist_ok=True)

        for filename in filenames:
            if filename.lower().endswith(supported_formats):
                img_path = os.path.join(dirpath, filename)
                thumb_path = os.path.join(thumb_dir, filename)

                # Skip if thumbnail already exists
                if os.path.exists(thumb_path):
                    print(f"Thumbnail already exists, skipping: {thumb_path}")
                    continue

                try:
                    with Image.open(img_path) as img:
                        img.thumbnail(thumbnail_size)
                        img.save(thumb_path)
                        print(f"Thumbnail created: {thumb_path}")
                except Exception as e:
                    print(f"Failed to create thumbnail for {img_path}: {e}")

