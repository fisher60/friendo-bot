"""The main bot module, contains all code for the bot application."""

import asyncio
import logging
import os
from pathlib import Path

LOG_FILE_PATH = Path.cwd() / "logs"
IMG_CACHE = Path.cwd() / "tmp"

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# create log directory
LOG_FILE_PATH.mkdir(exist_ok=True, parents=True)

# create image cache tmp directory
IMG_CACHE.mkdir(exist_ok=True, parents=True)

log_formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s: %(message)s")

FILE_HANDLER = logging.FileHandler(filename=Path(LOG_FILE_PATH, "friendo.log"), encoding="utf-8", mode="w")
FILE_HANDLER.setFormatter(log_formatter)
log.addHandler(FILE_HANDLER)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
log.addHandler(console_handler)

# On Windows, the selector event loop is required for aiodns.
if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

log.info("Cleaning out image_cache")

for file in IMG_CACHE.iterdir():
    if file.suffix == ".jpg":
        file.unlink()
