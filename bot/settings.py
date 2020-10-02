"""Constants for the bot."""

import os
from pathlib import Path

TOKEN = os.environ.get("FRIENDO_TOKEN")

MEME_USERNAME = os.environ.get("MEME_USERNAME")

MEME_PASSWORD = os.environ.get("MEME_PASSWORD")

COMMAND_PREFIX = "."

VERSION = "1.2."

NAME = "Friendo"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMG_CACHE = Path(BASE_DIR, "image_cache")

BASE_GITHUB_REPO = "https://github.com/fisher60/Friendo_Bot"
