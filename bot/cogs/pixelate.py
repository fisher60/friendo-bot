from collections import Counter
from io import BytesIO

import numpy as np
from discord import Color, Embed, File, Member
from discord.ext.commands import Cog, Context, command
from PIL import Image

from bot.bot import Friendo


class Pixelate(Cog):
    """Command for pixelating a user's avatar, defaults to the author if user not provided."""

    def __init__(self, bot: Friendo) -> None:
        self.bot = bot

    @staticmethod
    def dominant_color(image: Image) -> tuple:
        """Get the most occuring color in the image in rgb form as a tuple."""
        image = image.convert("RGB")
        arr = np.array(image)
        ls = []
        for pixel in arr:
            for rgb in pixel:
                ls.append(tuple(rgb))
        return Counter(ls).most_common(1)[0][0]

    @command(brief="Shows the pixelated avatar of the user/author",
             usage=".pixelate [user (optional)]",
             aliases=['pixel', 'blockify', 'pix'])
    async def pixelate(self, ctx: Context, user: Member = None) -> None:
        """Pixelate command, takes in an optional parameter user else pixelates author's avatar."""
        async with ctx.channel.typing():
            user = ctx.author.avatar if not user else user.avatar
            img_bytes = user.read()
            image = Image.open(BytesIO(await img_bytes))

            img_color = self.dominant_color(image)

            img_small = image.resize((24, 24), resample=Image.BILINEAR)
            result = img_small.resize((1024, 1024), Image.NEAREST)

            buffer = BytesIO()
            result.save(buffer, format="PNG")
            buffer.seek(0)

            img_file = File(buffer, filename="pixelated.png")
            img_url = 'attachment://pixelated.png'

            img_emb = Embed(color=Color.from_rgb(int(img_color[0]), int(img_color[1]), int(img_color[2])))
            img_emb.set_author(name="Here is your pixelated Image", icon_url=user)
            img_emb.set_image(url=img_url)

            await ctx.send(embed=img_emb, file=img_file)


async def setup(bot: Friendo) -> None:
    """Sets up the Pixelate cog."""
    await bot.add_cog(Pixelate(bot))
