from os import environ

TOKEN = environ.get("FRIENDO_TOKEN")

MEME_USERNAME = environ.get("MEME_USERNAME")

MEME_PASSWORD = environ.get("MEME_PASSWORD")

EVENT_API_KEY = environ.get("EVENT_API_KEY")

COMMAND_PREFIX = environ.get("COMMAND_PREFIX", ".")


WOLFRAM_APPID = environ.get("WOLFRAM_APPID")

VERSION = "1.2"

GITHUB_REPO = "https://github.com/fisher60/Friendo_Bot"

API_COGS = ["events", "memes"]
