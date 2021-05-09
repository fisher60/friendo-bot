# Friendo Bot
This is a Discord bot that comforts you when you are lonely, is there for you in the middle of the night, keeps you hydrated, and does all of your bidding like a ~~sexy~~ buttler with a true passion for what they do.

## Discord Bot Setup

To get a bot token go to [Discord Developer Portal](https://discord.com/developers/applications), create
 a new application and add a bot.

## Production Installation
1. `git clone <url>`

2. Create an [imgflip](https://api.imgflip.com/) api account

3. Create a [Ticketmaster](https://developer.ticketmaster.com/products-and-docs/apis/getting-started/) api account

4. Create a [Last.fm](https://www.last.fm/api) api account

5. Create a [Open Weather](https://openweathermap.org/price) api account (a free account works for this)

6. Get your AoC session cookie, see how - https://github.com/wimglenn/advent-of-code-wim/issues/1

7. Create a file `bot.env` in the root project directory and fill it out using the example below

8. `docker-compose up --build -d`

```text
# bot.env

FRIENDO_TOKEN = <your token here>
MEME_USERNAME = <your imgflip api username>
MEME_PASSWORD = <your imgflip api password>
EVENT_API_KEY = <your ticketmaster api key>
MUSIC_TOKEN = <your Last.fm api key>
WEATHER_TOKEN = <your open weather token>
AOC_SESSION_COOKIE = <your advent of code session cookie>
FRIENDO_API_USER = <your friendo api username>
FRIENDO_API_PASS = <your friendo api password>
FRIENDO_API_URL = <friendo api url>
```

## Dev Installation
* You can use the above docker method to run in a dev environment or the following pipenv (if using pipenv
the above environment variables must be added to the system or a file named `.env`).*

```bash
# Clone the repository on the develop branch
$ git clone -b "develop" https://github.com/fisher60/Friendo_Bot.git

# Navigate to the repository directory
$ cd Friendo_Bot

# Install pipenv through pip or your package manager
$ pip install pipenv

# Install the development and project dependencies
$ pipenv sync --dev

# Install pre-commit hooks
$ pipenv run pre-commit install

# Optionally: run pre-commit hooks to initialize them
$ pipenv run pre-commit run --all-files

# Enter the pipenv shell
$ pipenv shell

# Run the bot
$ pipenv run python -m bot
```
