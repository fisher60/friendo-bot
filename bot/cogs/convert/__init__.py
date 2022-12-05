import logging

from bot.bot import Friendo
from ._cog import Convert

logger = logging.getLogger("convert")


async def setup(bot: Friendo) -> None:
    """Sets up the Covert cog."""
    await bot.add_cog(Convert(bot))
