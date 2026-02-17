from io import BytesIO
from urllib import parse

import discord
from discord.ext import commands

from bot.settings import WOLFRAM_APPID


class Wolfram(commands.Cog):
    """Command for Wolfram search."""

    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.query = "http://api.wolframalpha.com/v2/{request}?{data}"

    @commands.command(
        brief="Takes in a wolfram search and displays the result",
        usage=".wolfram [query]",
        aliases=("wa", "wolframalpha"),
    )
    async def wolfram(self, ctx: commands.context, *, query: str) -> None:
        """Wolfram command, takes in a search and gives the result."""
        url_str = parse.urlencode(
            {
                "i": query,
                "appid": WOLFRAM_APPID,
            }
        )

        query_final = self.query.format(request="simple", data=url_str)

        async with ctx.channel.typing(), self.bot.session.get(query_final) as response:
            response.raise_for_status()
            image_bytes = await response.read()

            image_file = discord.File(BytesIO(image_bytes), filename="image.png")
            image_url = "attachment://image.png"

            message = ""
            footer = "View original for a bigger picture."
            color = discord.Colour.orange()

            final_emb = discord.Embed(title=message, color=color)
            final_emb.set_image(url=image_url)
            final_emb.set_footer(text=footer)

            await ctx.send(embed=final_emb, file=image_file)


async def setup(bot: commands.bot) -> None:
    """Sets up the Wolfram cog."""
    await bot.add_cog(Wolfram(bot))
