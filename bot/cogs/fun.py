from discord.ext.commands import Bot, Cog, command
from random import choice


class Fun(Cog):
    """commands for fun that offer no benefit to users."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        brief="Alternate case of inputted text",
        description="converts a phrase to alternating case",
        name="tosponge",
    )
    async def to_sponge(self, ctx, *, phrase):
        count = 0
        new = ""
        for i in phrase:
            if i == " ":
                new += i
            else:
                if count % 2 == 0:
                    new += i
                if count % 2 == 1:
                    new += i.upper()
                count += 1

        await ctx.send(new)
        return new

    @command(
        brief="simulates a coin toss",
        description="gives an output of heads or tails like a coin",
        name="flip",
    )
    async def coin_toss(self, ctx, toss):
        outcomes = ["heads", "tails"]

        if toss == choice(outcomes):
            msg = f"{ctx.author.mention} wins!"
        else:
            msg = f"{ctx.author.mention} loses!"

        await ctx.send(msg)


def setup(bot: Bot) -> None:
    """Load the Fun cog."""
    bot.add_cog(Fun(bot))
