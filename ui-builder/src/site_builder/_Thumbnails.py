import os
import subprocess

from PIL import Image


def format_thumbnails(thumbnail_path):
    """
    Format the thumbnail to be a 200x200 thumbnail
    """
    all_thumbnail_files = os.listdir(thumbnail_path)
    for file in all_thumbnail_files:
        this_thumbnail = Image.open(thumbnail_path + file)
        cropped_thumbnail = square_image(this_thumbnail)
        cropped_thumbnail.save(thumbnail_path + file)


def square_image(img):
    width, height = img.size
    new_dim = min(width, height)

    left = (width - new_dim) / 2
    top = (height - new_dim) / 2
    right = (width + new_dim) / 2
    bottom = (height + new_dim) / 2

    return img.crop((left, top, right, bottom))
