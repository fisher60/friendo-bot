from discord.ext.commands import Cog, Context, command

from bot.bot import Freindo


class FibonacciSequence(Cog):
    """The standard Fibonacci Sequence."""

    def __init__(self, bot: Freindo) -> None:
        self.bot = bot

    @command(brief="It adds the last two previous numbers and appends the output", ignore_extra=True,
            name="gen_fib")
    async def generate_fib(limit:int):
        """Generates Fibonacci Sequence for the specified limit.
        for eg if limit is 5 it would generate 1,1,2,3,5, the max limit is 1000
        """
        if limit > 1000:
            limit = 1000

        fib_seq = [1, 1]

        for index in range(1,limit-1):
            fib_seq.append(fib_seq[index] + fib_seq[index-1])
        
        fib_seq = list(map(lambda nums: str(nums), fib_seq))

        return ' '.join(fib_seq)


def setup(bot: Friendo) -> None:
    """Load the Utilities cog."""
    bot.add_cog(FibonacciSequence(bot))
