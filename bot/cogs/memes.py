from discord.ext.commands import Bot, Cog, command
from bot.meme_api import memegen


class Memes(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(brief="[command] [*args]", description=".meme search [keywords] to search for available memes\n."
                                                    ".meme create [meme name from meme search]; [text]; [text]; ...\n"
                                                    "----each [text] should be the text to enter into a text box, "
                                                    "do not exceed the max number of text boxes")
    async def meme(self, ctx, arg1, *, args):
        args = args.split("; ")
        this_meme = memegen.Meme()
        if arg1 == "create":
            name, text = args[0], args[1:]
            await ctx.send(this_meme.generate_meme(name=name, text=text))
        elif arg1 == "search":
            await ctx.send(this_meme.search_meme_list(args))
        return 'test success'


def setup(bot: Bot) -> None:
    """Load the Memes cog."""
    bot.add_cog(Memes(bot))
