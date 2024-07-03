import os

from PIL import Image


def get_image_info(image_path) -> tuple:
    image = Image.open(image_path)
    w, h = image.size

    filename, file_extension = os.path.splitext(image_path)

    return w, h, file_extension
