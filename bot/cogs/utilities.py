from discord.ext.commands import Bot, Cog, command
from bot import settings


class Utilities(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def version(self, ctx):
        msg = f"Version is {settings.VERSION}"
        await ctx.send(msg)
        return msg

    @command()
    async def version(self, ctx):
        msg = f"Version is {settings.VERSION}"
        await ctx.send(msg)
        return msg


def setup(bot: Bot) -> None:
    """Load the Help cog."""
    bot.add_cog(Utilities(bot))