"""
The main bot module, contains all code for the bot application.
"""

import logging
import os

from .settings import IMG_CACHE, LOG_FILE_NAME

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
FILE_HANDLER = logging.FileHandler(filename=LOG_FILE_NAME, encoding="utf-8", mode="w")
FILE_HANDLER.setFormatter(
    logging.Formatter("%(levelname)s:%(asctime)s:%(name)s: %(message)s")
)
logger.addHandler(FILE_HANDLER)

logger.info("Cleaning out image_cache")

img_dir = os.listdir(IMG_CACHE)
for file in img_dir:
    if file.endswith(".jpg"):
        os.remove(os.path.join(IMG_CACHE, file))
