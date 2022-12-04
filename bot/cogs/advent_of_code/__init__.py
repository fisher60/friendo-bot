import logging

from bot.bot import Friendo
from bot.settings import AOC_JOIN_CODE
from ._cog import AdventOfCode

logger = logging.getLogger("advent_of_code")


async def setup(bot: Friendo) -> None:
    """Sets up the AdventOfCode cog."""
    if AOC_JOIN_CODE is not None:
        await bot.add_cog(AdventOfCode(bot))
    else:
        logger.warning("Skipping setup for advent of code as a `AOC_JOIN_CODE` wasn't provided")
