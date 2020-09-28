from discord.ext.commands import Bot, Cog, command
from cv2 import imwrite, imread, cvtColor, COLOR_BGR2RGB
import aiohttp
import aiofiles
from pathlib import Path

from bot.settings import IMG_CACHE


class Segmentation(Cog):
    """Simple aks-reply commands, good for testing or making members feel welcome."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    async def download_image(url) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(Path(IMG_CACHE, "temp_img.jpg"), mode="wb")
                    await f.write(await resp.read())
                    await f.close()
                    return True
                else:
                    return False

    @command(
        brief="Send an image and get a segmented one back",
        description="Invoke this command and specify your options to get a segmented image back.",
    )
    async def segment(self, ctx):
        attachments = ctx.message.attachments
        if len(attachments):
            img_url = attachments[0].url
            success = await self.download_image(url=img_url)
            if success:
                pass
            else:
                await ctx.send("Image could not be processed")
        else:
            await ctx.send("Attatch an image, mate.")


def setup(bot: Bot) -> None:
    """Load the Image Segmentation cog."""
    bot.add_cog(Segmentation(bot))
