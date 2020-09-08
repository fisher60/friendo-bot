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
*You can use the above docker method to run in a dev environment or the following pipenv (if using pipenv 
the above environment variables must be added to the system/a .env file).*

1. `git clone -b "feature-branch-name" <url>` this repo

2. `pip install pipenv`

3. Set up environment variables, this can be done by adding a file named `.env` 
(make sure the file name is exactly `.env`) to the root directory with the variables from the above `bot.env` example,
 or add the same environment variables to the system (`.env` is the recommended 
approach).

4. `pipenv sync` to install project dependencies.

5. `pipenv shell` to activate virtual environment 

6. run `python -m bot` to start the bot

