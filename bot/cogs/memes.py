from asyncio import sleep
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
        response = None

        if arg1 == "create":
            name, text = args[0], args[1:]
            result = this_meme.generate_meme(name=name, text=text)
            if result:
                await ctx.message.delete()
                await ctx.send(result)
            else:
                response = await ctx.send("Meme could not be created")
                await ctx.message.delete(delay=8)
                await response.delete(delay=8)

        elif arg1 == "search":
            result = this_meme.search_meme_list(args)
            if result:
                response = await ctx.send(result)
                await response.delete(delay=30)
            else:
                response = await ctx.send("No results for that search")
                await ctx.message.delete(delay=8)
                await response.delete(delay=8)

        return 'test success'


def setup(bot: Bot) -> None:
    """Load the Memes cog."""
    bot.add_cog(Memes(bot))
