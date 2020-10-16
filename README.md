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

5. Create a file `bot.env` in the root project directory and fill it out using the example below

6. `docker-compose up --build -d`

```text
# bot.env

FRIENDO_TOKEN = <your token here>
MEME_USERNAME = <your imgflip api username>
MEME_PASSWORD = <your imgflip api password>
EVENT_API_KEY = <your ticketmaster api key>
MUSIC_TOKEN = <your Last.fm api key>
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

## Command Line Arguments

1. Suppreses the loading of cogs that requires external API ie. events and memes cogs
```bash
$ pipenv run python -m bot --no-api
```
2. Disable certain cogs and enables all other cogs
```bash
# disables events fun greetings cogs and enables all other cogs
$ pipenv run python -m bot --disable events fun greetings
```
3. Enable certain cogs and disable all other cogs
```bash
# enables events fun greetings cogs and disables all other cogs
$ pipenv run python -m bot --enable events fun greetings
```
