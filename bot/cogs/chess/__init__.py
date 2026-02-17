import logging
from typing import TYPE_CHECKING

from ._cog import Chess

if TYPE_CHECKING:
    from bot.bot import Friendo

logger = logging.getLogger("chess")


async def setup(bot: Friendo) -> None:
    """Adding the chess cog."""
    await bot.add_cog(Chess(bot))
