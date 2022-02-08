import random

from disnake.ext.commands import Cog, Context, command

from bot.bot import Friendo


class RandomCase(Cog):
    """A command that randomizes the cases of every letter of a word or words."""

    def __init__(self, bot: Friendo) -> None:
        self.bot = bot

    @command(brief="Randomize case of string")
    async def randomcase(self, ctx: Context, *, string: str = None) -> None:
        """Scrambles a string."""
        randomized_string = "".join(
            [random.choice((_.upper(), _.lower())) for _ in string]
        )

        await ctx.send(f">>> {randomized_string}")


def setup(bot: Friendo) -> None:
    """Load the Utilities cog."""
    bot.add_cog(RandomCase(bot))
