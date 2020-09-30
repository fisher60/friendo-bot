"""
Launches the bot, starts the asyncio loop when called.
"""
from bot.meme_api import memegen
from . import settings
from .bot import Bot


if __name__ == "__main__":
    bot = Bot(command_prefix=settings.COMMAND_PREFIX)

    @bot.event
    async def on_ready():
        """
        Runs when the bot is connected.
        """
        print("Logged in as")
        print(bot.user.name)
        print(bot.user.id)
        print("------")

    memegen.Meme()

    # load in basic commands
    bot.load_extension("bot.cogs.greetings")
    bot.load_extension("bot.cogs.utilities")
    bot.load_extension("bot.cogs.source")

    # load in Meme commands
    bot.load_extension("bot.cogs.memes")

    # load in Admin commands
    bot.load_extension("bot.cogs.admin")

    # load in Fun commands
    bot.load_extension("bot.cogs.fun")
    bot.run(settings.TOKEN)
