import logging
from typing import TYPE_CHECKING

from bot.settings import AOC_JOIN_CODE

from ._cog import AdventOfCode

if TYPE_CHECKING:
    from bot.bot import Friendo

logger = logging.getLogger("advent_of_code")


async def setup(bot: Friendo) -> None:
    """Sets up the AdventOfCode cog."""
    if AOC_JOIN_CODE is not None:
        await bot.add_cog(AdventOfCode(bot))
    else:
        logger.warning("Skipping setup for advent of code as a `AOC_JOIN_CODE` wasn't provided")
