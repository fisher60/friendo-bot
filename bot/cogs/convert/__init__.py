from typing import TYPE_CHECKING

from ._cog import Convert

if TYPE_CHECKING:
    from bot.bot import Friendo


async def setup(bot: Friendo) -> None:
    """Sets up the Convert cog."""
    await bot.add_cog(Convert(bot))
