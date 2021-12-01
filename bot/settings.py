from os import environ

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

FRIENDO_API_USER = environ.get("FRIENDO_API_USER")
FRIENDO_API_PASS = environ.get("FRIENDO_API_PASS")
FRIENDO_API_URL = environ.get("FRIENDO_API_URL", "http://dev.friendo.us/api/")

VERSION = "1.2"

GITHUB_REPO = "https://github.com/fisher60/Friendo_Bot"

AOC_LEADERBOARD_LINK = "https://adventofcode.com/2020/leaderboard/private/view/442826.json"

API_COGS = ["events", "memes"]
