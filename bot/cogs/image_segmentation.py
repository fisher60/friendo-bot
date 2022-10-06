from functools import partial
from os import remove
from pathlib import Path
from typing import List, Optional

import aiofiles
from cv2 import COLOR_BGR2RGB, cvtColor, imread
import discord
from discord.ext.commands import Cog, Context, command
import matplotlib.pyplot as plt
from skimage.color import rgb2hsv
from numpy import ndarray

from bot.bot import Friendo


class Segmentation(Cog):
    """Commands for returning a segmented image back to a user."""

    def __init__(self, bot: Friendo) -> None:
        self.bot = bot
        self.img_queue = []

    async def download_image(self, url: str) -> Optional[str]:
        """
        Download a discord attachment using the CDN url.

        Returns the file name if successful, else it returns None.
        """
        async with self.bot.session.get(url) as resp:
            if resp.status == 200:
                file_name = f"temp_img_{len(self.img_queue)}.jpg"
                self.img_queue.append(file_name)
                f = await aiofiles.open(
                    Path.cwd() / file_name,
                    mode="wb",
                )
                await f.write(await resp.read())
                await f.close()

                return file_name

    @staticmethod
    def delete_image(file_name: str) -> None:
        """Deletes an image."""
        remove(Path.cwd() / file_name)

    @staticmethod
    def save_image(file_name: str, array: List[str]) -> None:
        """Saves the image from the MatPlotLib plot."""
        plt.imsave(Path.cwd() / file_name, array)

    @staticmethod
    def hsv_image(file_name: str) -> ndarray:
        """Converts color data of a image."""
        rgb_img = cvtColor(imread(str(Path.cwd() / file_name)), COLOR_BGR2RGB)

        return rgb2hsv(rgb_img)

    def hue_image(self, file_name: str) -> str:
        """Change hue of image."""
        hsv_img = self.hsv_image(file_name)

        self.save_image(file_name, hsv_img[:, :, 0])

        return file_name

    @command(
        brief="Send an image and get a segmented one back",
        description="Invoke this command and specify your options to get a segmented image back.",
    )
    async def segment(self, ctx: Context, img_format: str = None) -> None:
        """
        Takes a discord attachment and an optional argument 'img_format'.

        Sends the same attachment in the specified format.
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
                    output_image = discord.File(Path.cwd() / processed_image)
                    await ctx.send(file=output_image)

                self.delete_image(file_name)

            # Download failed
            else:
                await ctx.send("Image could not be processed")

        # No attachment
        else:
            await ctx.send("Attach an image, mate.")


async def setup(bot: Friendo) -> None:
    """Load the Image Segmentation cog."""
    await bot.add_cog(Segmentation(bot))
