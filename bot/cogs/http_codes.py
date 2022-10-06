from random import choice

from discord.ext.commands import Cog, Context, command

from bot.bot import Friendo


class HttpCodes(Cog):
    """Get 'funny' images for each HTTP error code."""

    def __init__(self, bot: Friendo) -> None:
        self.bot = bot

    @command(
        brief="Get a cat http image from a http code.",
        aliases=["httpcat", "statuscat", "status_cat"]
    )
    async def http_cat(self, ctx: Context, code: int) -> None:
        """Get a cat http image from a http code."""
        await ctx.send(f"https://http.cat/{code}")

    @command(
        brief="Get a dog http image from a http code.",
        aliases=["httpdog", "statusdog", "status_dog"]
    )
    async def http_dog(self, ctx: Context, code: int) -> None:
        """Get a dog http image from a http code."""
        await ctx.send(f"https://http.dog/{code}.jpg")

    @command(
        brief="Get a dog or cat http image from a http code.",
        aliases=["status"]
    )
    async def http(self, ctx: Context, code: int) -> None:
        """Get a dog or cat http image from a http code."""
        random_handler = choice((self.http_dog, self.http_cat))
        await random_handler(ctx, code)


def setup(bot: Friendo) -> None:
    """Load the HttpCodes cog."""
    bot.add_cog(HttpCodes(bot))
