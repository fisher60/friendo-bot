"""The main bot module, contains all code for the bot application."""

import logging
import os
from pathlib import Path

from .settings import IMG_CACHE, LOG_FILE_PATH

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not os.path.exists(LOG_FILE_PATH):
    os.makedirs(LOG_FILE_PATH)

FILE_HANDLER = logging.FileHandler(
    filename=Path(LOG_FILE_PATH, "friendo.log"), encoding="utf-8", mode="w"
)

FILE_HANDLER.setFormatter(
    logging.Formatter("%(levelname)s:%(asctime)s:%(name)s: %(message)s")
)

logger.addHandler(FILE_HANDLER)

logger.info("Cleaning out image_cache")

img_dir = os.listdir(IMG_CACHE)
for file in img_dir:
    if file.endswith(".jpg"):
        os.remove(os.path.join(IMG_CACHE, file))
