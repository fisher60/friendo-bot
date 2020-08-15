# Friendo Bot
This is a Discord bot that comforts you when you are lonely, is there for you in the middle of the night, keeps you hydrated, and does all of your bidding like a ~~sexy~~ buttler with a true passion for what they do.

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
1. `git clone -b "feature-branch-name" <url>` this repo

2. `virtualenv venv` to create a virtual environement named "venv" and activate it (the name "venv" is for the .gitignore)

3. `pip install -r requirements.txt`

4. to run use `python -m bot`

