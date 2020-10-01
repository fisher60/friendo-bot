import os
from .settings import IMG_CACHE


def clean_image_cache():
    print("Cleaning out image_cache")
    img_dir = os.listdir(IMG_CACHE)
    for file in img_dir:
        if file.endswith(".jpg"):
            os.remove(os.path.join(IMG_CACHE, file))
