import logging
from os import environ

log = logging.getLogger(__name__)

TOKEN = environ.get("FRIENDO_TOKEN")

MEME_USERNAME = environ.get("MEME_USERNAME")

MEME_PASSWORD = environ.get("MEME_PASSWORD")

EVENT_API_KEY = environ.get("EVENT_API_KEY")

COMMAND_PREFIX = environ.get("COMMAND_PREFIX", ".")

MUSIC_TOKEN = environ.get("MUSIC_TOKEN")

WOLFRAM_APPID = environ.get("WOLFRAM_APPID")

WEATHER_TOKEN = environ.get("WEATHER_TOKEN")

AOC_SESSION_COOKIE = environ.get("AOC_SESSION_COOKIE")
AOC_JOIN_CODE = environ.get("AOC_JOIN_CODE")
if AOC_JOIN_CODE:
    AOC_LEADERBOARD_ID = AOC_JOIN_CODE.split("-")[0]
else:
    AOC_LEADERBOARD_ID = None

FRIENDO_API_USER = environ.get("FRIENDO_API_USER")
FRIENDO_API_PASS = environ.get("FRIENDO_API_PASS")
FRIENDO_API_URL = environ.get("FRIENDO_API_URL", "http://dev.friendo.dev/api/")

GIT_SHA = environ.get("GIT_SHA", "development")

log.info(f"Using {FRIENDO_API_URL} for backend...")

VERSION = "1.2"

GITHUB_REPO = "https://github.com/fisher60/friendo-bot"

API_COGS = ["events", "memes"]
