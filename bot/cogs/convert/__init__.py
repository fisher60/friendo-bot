from bot.bot import Friendo
from ._cog import Convert


async def setup(bot: Friendo) -> None:
    """Sets up the Convert cog."""
    await bot.add_cog(Convert(bot))
