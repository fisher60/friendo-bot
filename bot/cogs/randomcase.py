import random
from itertools import cycle

from discord.ext.commands import Cog, Context, command

from bot.bot import Friendo


_func = cycle((str.upper, str.lower))
BASE_CHANCE_TO_SKIP = 0.1
PROGRESSION_STEP = 0.05


class RandomCase(Cog):
    """A command that randomizes the cases of every letter of a word or words."""

    def __init__(self):
        self.chance_to_skip = BASE_CHANCE_TO_SKIP

    def randomize(self, letter: str) -> str:
        """
        Cycles though upper and lower, with a chance to skip.

        Progressively increases the chance to skip a cycle.
        """
        if random.random() > self.chance_to_skip:
            next(_func)
            self.chance_to_skip = BASE_CHANCE_TO_SKIP
        else:
            self.chance_to_skip += PROGRESSION_STEP
        return next(_func)(letter)

    @command(brief="Randomize case of string")
    async def randomcase(self, ctx: Context, *, string: str = None) -> None:
        """Scrambles a string."""
        randomized_string = "".join(
            self.randomize(letter) for letter in string
        )

        await ctx.send(f">>> {randomized_string}")


def setup(bot: Friendo) -> None:
    """Load the Utilities cog."""
    bot.add_cog(RandomCase())
