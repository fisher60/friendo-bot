import discord
import asyncio
from . import settings
from .bot import Bot


if __name__ == "__main__":
    bot = Bot(command_prefix=settings.COMMAND_PREFIX)

    @bot.event
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')

    # load in basic commands
    bot.load_extension("bot.cogs.greetings")
    bot.load_extension("bot.cogs.utilities")

    # load in Admin commands
    bot.load_extension("bot.cogs.admin")

    bot.run(settings.TOKEN)
