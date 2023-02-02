import logging

from bot.bot import Friendo
from ._cog import Chess

logger = logging.getLogger("chess")


async def setup(bot: Friendo) -> None:
    """Adding the chess cog."""
    await bot.add_cog(Chess(bot))
