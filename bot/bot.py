import asyncio

import aiohttp
from discord.ext import commands

from .settings import NAME


class Bot(commands.Bot):
    """Base Class for the discord bot."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setting the loop.
        self.loop = asyncio.get_event_loop()

        # Creating session for web requests.
        self.session = aiohttp.ClientSession()

    def __str__(self):
        """Returns the name of the bot."""
        return NAME

    async def on_ready(self):
        """Runs when the bot is connected."""
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")
