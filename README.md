# Friendo Bot
This is a Discord bot that comforts you when you are lonely, is there for you in the middle of the night, keeps you hydrated, and does all of your bidding like a ~~sexy~~ buttler with a true passion for what they do.

## Discord Bot Setup

To get a bot token go to [Discord Developer Portal](https://discord.com/developers/applications), create
 a new application and add a bot.

## Production Installation
1. `git clone <url>`

2. Create an [imgflip](https://api.imgflip.com/) api account

3. Create a file `bot.env` in the root project directory and fill it out using the example below

4. `docker-compose up --build -d`

```text
# bot.env

FRIENDO_TOKEN = <your token here>
MEME_USERNAME = <your imgflip api username>
MEME_PASSWORD = <your imgflip api password>
```

## Dev Installation
* You can use the above docker method to run in a dev environment or the following pipenv (if using pipenv 
the above environment variables must be added to the system/a .env file).*

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
