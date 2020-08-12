from discord.ext.commands import Bot, Cog, command


class Greetings(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def hello(self, ctx):
        msg = f"Hello! {ctx.author.mention}"
        await ctx.send(msg)
        return msg


def setup(bot: Bot) -> None:
    """Load the Help cog."""
    bot.add_cog(Greetings(bot))
