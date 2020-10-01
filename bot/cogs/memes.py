"""Commands for using the meme generator module"""
from discord.ext.commands import Bot, Cog, command
from bot.meme_api import memegen


class Memes(Cog):
    """Commands for using the Meme Generator."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.this_meme = memegen.Meme(bot)

    @command(
        brief="commands for using the meme generator. [command] [*args]",
        description=".meme search [keywords] to search for available memes\n."
        ".meme create [meme name from meme search]; [text]; [text]; ...\n"
        "----each [text] should be the text to enter into a text box, "
        "do not exceed the max number of text boxes",
    )
    async def meme(self, ctx, arg1, *, args):
        """The main command, used to parse and process the command arguments"""

        args = args.split("; ")

        if arg1 == "create":
            # Creates a new meme

            name, text = args[0], args[1:]
            result = await self.this_meme.generate_meme(name=name, text=text)
            if result:
                await ctx.send(result)
            else:
                response = await ctx.send("Meme could not be created")
                await ctx.message.delete(delay=8)
                await response.delete(delay=8)

        elif arg1 == "search":
            # searches the cached meme_list for keywords and returns matching meme names

            result = self.this_meme.search_meme_list(args)
            if result:
                response = await ctx.send(result)
                await ctx.message.delete(delay=30)
                await response.delete(delay=30)
            else:
                response = await ctx.send("No results for that search")
                await ctx.message.delete(delay=8)
                await response.delete(delay=8)

        return "test success"


def setup(bot: Bot) -> None:
    """Load the Memes cog."""
    bot.add_cog(Memes(bot))
