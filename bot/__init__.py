"""The main bot module, contains all code for the bot application."""

import asyncio
import logging
import os
from pathlib import Path

LOG_FILE_PATH = Path.cwd() / 'logs'
IMG_CACHE = Path.cwd() / 'tmp'

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# create log directory
if not os.path.exists(LOG_FILE_PATH):
    os.makedirs(LOG_FILE_PATH)

# create image cache tmp directory
if not os.path.exists(IMG_CACHE):
    os.makedirs(IMG_CACHE)

log_formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s: %(message)s")

FILE_HANDLER = logging.FileHandler(
    filename=Path(LOG_FILE_PATH, "friendo.log"), encoding="utf-8", mode="w"
)
FILE_HANDLER.setFormatter(log_formatter)
log.addHandler(FILE_HANDLER)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
log.addHandler(console_handler)

# On Windows, the selector event loop is required for aiodns.
if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

log.info("Cleaning out image_cache")

img_dir = os.listdir(IMG_CACHE)
for file in img_dir:
    if file.endswith(".jpg"):
        os.remove(os.path.join(IMG_CACHE, file))
