import asyncio
from asyncio import sleep
from discord.ext import tasks
from discord.ext.commands import Bot, Cog, command


def fibo_send(n):
    a, b = 0, 1
    sequence = []
    while a < n:
        sequence.append(a)
        a, b = b, a + b
    return "".join(str(x) + " " for x in sequence)


class Fibonacci(Cog):
    """A simple command to create a fibonacci number from input."""

    @command(brief="Calculates the fibonacci sequence given by an input")
    async def fib(self, ctx, num):
        try:
            f = fibo_send(int(num))
            await ctx.send(f"Fibonacci sequence:\n{f}")
        except ValueError:
            await ctx.send("Not a number. Input should be like: `.fib 10`")


def setup(bot: Bot) -> None:
    """Load the Fibonacci cog."""
    bot.add_cog(Fibonacci(bot))
