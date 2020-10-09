import asyncio
import logging
import traceback

import aiohttp
from discord.ext import commands

from .settings import NAME

logger = logging.getLogger(__name__)


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
        logger.info("Logged in as")
        logger.info(self.user.name)
        logger.info(self.user.id)
        logger.info("------")

    async def on_command_error(self, ctx, exception):
        """Fired when exception happens."""
        logger.error(
            "Exception happened while executing command",
            exc_info=(type(exception), exception, exception.__traceback__),
        )

    async def logout(self) -> None:
        """Making sure connections are closed properly."""
        await self.session.close()

        return await super().logout()
