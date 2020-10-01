import aiohttp
import aiofiles
import discord
import matplotlib.pyplot as plt
from cv2 import imread, cvtColor, COLOR_BGR2RGB
from discord.ext.commands import Bot, Cog, command
from functools import partial
from os import remove
from pathlib import Path
from skimage.color import rgb2hsv

from bot.settings import IMG_CACHE


class Segmentation(Cog):
    """Commands for returning a segmented image back to a user."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.img_queue = []

    async def download_image(self, url) -> str or None:
        """
        Download a discord attatchment using the CDN url.

        Returns the file name if successful, else it returns None.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    file_name = f"temp_img_{len(self.img_queue)}.jpg"
                    self.img_queue.append(file_name)
                    f = await aiofiles.open(
                        Path(IMG_CACHE, file_name),
                        mode="wb",
                    )
                    await f.write(await resp.read())
                    await f.close()

                    return file_name

                else:
                    return None

    @staticmethod
    def delete_image(file_name):
        remove(Path(IMG_CACHE, file_name))

    @staticmethod
    def save_image(file_name, array):
        plt.imsave(Path(IMG_CACHE, file_name), array)

    @staticmethod
    def hsv_image(file_name: str):
        rgb_img = cvtColor(imread(str(Path(IMG_CACHE, file_name))), COLOR_BGR2RGB)
        return rgb2hsv(rgb_img)

    def hue_image(self, file_name: str) -> str:
        hsv_img = self.hsv_image(file_name)
        self.save_image(file_name, hsv_img[:, :, 0])
        return file_name

    @command(
        brief="Send an image and get a segmented one back",
        description="Invoke this command and specify your options to get a segmented image back.",
    )
    async def segment(self, ctx, img_format=None) -> None:
        """
        Takes a discord attatchment and an optional argument 'img_format'.
        Sends the same attatchment in the specified format
        """
        processed_image = None
        attachments = ctx.message.attachments

        if len(attachments):
            img_url = attachments[0].url
            file_name = await self.download_image(url=img_url)

            # Download was successful
            if file_name:
                if img_format in [None, "hue"]:
                    to_exec = partial(self.hue_image, file_name)
                    processed_image = await self.bot.loop.run_in_executor(None, to_exec)
                else:
                    await ctx.send("Please choose a valid image format")

                # Input was valid
                if processed_image:
                    output_image = discord.File(Path(IMG_CACHE, processed_image))
                    await ctx.send(file=output_image)

                self.delete_image(file_name)

            # Download failed
            else:
                await ctx.send("Image could not be processed")

        # No attatchement
        else:
            await ctx.send("Attatch an image, mate.")


def setup(bot: Bot) -> None:
    """Load the Image Segmentation cog."""
    bot.add_cog(Segmentation(bot))
