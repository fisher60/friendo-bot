"""Commands that greet users, meant as an example/base for writing new cogs."""
from discord.ext.commands import Bot, Cog, command


class Greetings(Cog):
    """Simple ask-reply commands, good for testing or making members feel welcome."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(brief="Say hello")
    async def hello(self, ctx):
        """Tells a user 'hello'"""
        msg = f"Hello! {ctx.author.mention}"
        await ctx.send(msg)
        return msg


def setup(bot: Bot) -> None:
    """Load the Greetings cog."""
    bot.add_cog(Greetings(bot))
