from discord.ext.commands import Bot, Cog, command
from bot.meme_api import memegen


class Memes(Cog):
    """Commands for using the Meme Generator."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        brief="meme generator commands. Usage: `.meme [command] [*args]`",
        description="`.meme search [keywords]` to keyword search for related memes\n"
                    "`.meme create [valid meme name]; [text]; [text]; ...` to create a new meme\n"
                    "find a valid meme name with `meme search` before using `meme create`\n"
                    "supply more arguments to add text boxes in the meme\n"
                    "exceeding the max text boxes will cause generation to fail",
    )
    async def meme(self, ctx, arg1, *, args):
        """The main command, used to parse and process the command arguments"""

        args = args.split("; ")
        this_meme = memegen.Meme()
        response = None

        if arg1 == "create":
            # Creates a new meme

            name, text = args[0], args[1:]
            result = this_meme.generate_meme(name=name, text=text)
            if result:
                await ctx.send(result)
            else:
                response = await ctx.send("Meme could not be created")
                await ctx.message.delete(delay=8)
                await response.delete(delay=8)

        elif arg1 == "search":
            # searches the cached meme_list for keywords and returns matching meme names

            result = this_meme.search_meme_list(args)
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
