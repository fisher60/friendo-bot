"""Constants for the bot."""

import os

TOKEN = os.environ.get("FRIENDO_TOKEN")

MEME_USERNAME = os.environ.get("MEME_USERNAME")

MEME_PASSWORD = os.environ.get("MEME_PASSWORD")

COMMAND_PREFIX = "."

VERSION = "1.2.8"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_GITHUB_REPO = "https://github.com/fisher60/Friendo_Bot"
