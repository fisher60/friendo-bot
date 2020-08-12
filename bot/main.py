import discord
import asyncio
import bot.settings as settings
from bot.bot import Bot

if __name__ == "__main__":
    bot = Bot()

    bot.load_extension("bot.cogs.greetings")

    bot.run(settings.TOKEN)
