from discord.ext.commands import Bot, Cog, command


class Greetings(Cog):
    """Simple aks-reply commands, good for testing or making members feel welcome."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def hello(self, ctx):
        msg = f"Hello! {ctx.author.mention}"
        await ctx.send(msg)
        return msg


def setup(bot: Bot) -> None:
    """Load the Greetings cog."""
    bot.add_cog(Greetings(bot))
