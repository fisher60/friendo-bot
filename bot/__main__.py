import asyncio
import inspect
import pkgutil
import socket
from typing import Iterator, NoReturn

import aiohttp
from discord import AllowedMentions, Intents

from bot import cogs
from bot import settings
from bot.bot import Friendo


def _get_cogs() -> Iterator[str]:
    """
    Return an iterator going through each cog.

    On each iteration the cog is check for having a setup function raising a more readable error if not found.
    """

    def on_error(name: str) -> NoReturn:
        raise ImportError(name=name)

    for module in pkgutil.walk_packages(cogs.__path__, f"{cogs.__name__}.", onerror=on_error):
        if module.ispkg:
            _import = __import__(module.name)
            if not inspect.isfunction(getattr(_import, "setup", None)):
                continue

        yield module.name


async def start_bot() -> None:
    """Load in extensions and start running the bot."""
    resolver = aiohttp.AsyncResolver()
    connector = aiohttp.TCPConnector(
        resolver=resolver,
        family=socket.AF_INET,
    )
    async with aiohttp.ClientSession(connector=connector) as session:
        bot = Friendo(
            command_prefix=settings.COMMAND_PREFIX, help_command=None, intents=Intents.all(),
            allowed_mentions=AllowedMentions(everyone=False),
            session=session,
            connector=connector,
            resolver=resolver,
        )
        for cog in _get_cogs():
            await bot.load_extension(cog)

        async with bot:
            await bot.start(settings.TOKEN)

if __name__ == "__main__":
    asyncio.run(start_bot())
