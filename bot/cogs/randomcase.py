"""Commands that provide some sort of service to a user."""
from asyncio import sleep
import subprocess
from discord.ext import tasks
from discord.ext.commands import Bot, Cog, command
from bot import settings
import random


class RandomCase(Cog):
    """A command that randomizes the cases of every letter of a word or words."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(brief="Randomize case of string")
    async def randomcase(
        self, ctx, *, string=None
    ):  # Though not pythonic named but I hope owner will consider
        randomized_string = "".join(
            [random.choice((_.upper(), _.lower())) for _ in string]
        )
        await ctx.send(f">>> {randomized_string}")


def setup(bot: Bot) -> None:
    """Load the Utilities cog."""
    bot.add_cog(RandomCase(bot))
