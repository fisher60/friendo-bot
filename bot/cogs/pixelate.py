import discord
from discord import Color, Embed
from PIL import Image
from io import BytesIO
from discord.ext import commands


class Pixelate(commands.Cog):
    """Command for pixelating a user's avatar, defaults to the author if user not provided."""

    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(brief="Shows the pixelated avatar of the user/author",
                      usage=".pixelate [user (optional)]",
                      aliases=['pixel', 'blockify', 'pix'])
    async def pixelate(self, ctx: commands.context, user: discord.Member = None) -> None:
        """Pixelate command, takes in an optional parameter user else pixelates author's avatar."""
        async with ctx.channel.typing():
            user = user
            img_bytes = ctx.author.avatar_url.read() if not user else user.avatar_url.read()
            image = Image.open(BytesIO(await img_bytes))

            img_small = image.resize((16, 16), resample=Image.BILINEAR)
            result = img_small.resize((1024, 1024), Image.NEAREST)

            buffer = BytesIO()
            result.save(buffer, format="PNG")
            buffer.seek(0)

            img_file = discord.File(buffer, filename="pixelated.png")
            img_url = 'attachment://pixelated.png'

            img_emb = Embed(color=Color.blue())
            img_emb.set_footer(text="Here is your pixelated image")
            img_emb.set_image(url=img_url)

            await ctx.send(embed=img_emb, file=img_file)


def setup(bot: commands.bot) -> None:
    """Sets up the Pixelate cog."""
    bot.add_cog(Pixelate(bot))
