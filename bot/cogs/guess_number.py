import discord
import math, random
from discord.ext.commands import Bot, Cog, command
# from discord.ext import commands

#bot_prefix = "."

#client = commands.Bot(command_prefix=bot_prefix)

class GuessGame(Cog): # Change class name if needed.
    """Commands for Guessing Right Number"""

    def __init__(self, bot: Bot):
        self.bot = bot

    # Variables in class GuessGame
    lower_bound = 1
    upper_bound = 10

    ### Results in terminal
    #@client.event
    #async def on_ready(self):
    #    print('Bot is ready.')

    ### Commands
    @command(
        brief="Use `.bound n1 n2` to set your bound.\n use `.bound d` to default bounds.",
        description = "n1 => lower_bound, n2 => upper_bound\n Example: `.bound 1 10` will set the bound to 1 and 10.\n(1,100) is the default."
    )
    # Set up the bounds.  Optional.  (1,100) is the default.
    async def bound(self, ctx, lower, *,upper): # Will set bound when called.
        # Default bounds unless it's rewritten with .bound command
        lower_bound = 1
        upper_bound = 10

        if lower == 'd': # In case someone want to change it back to default
            GuessGame.lower_bound = lower_bound
            GuessGame.upper_bound = upper_bound
            await ctx.send(f'The bounds are now default. Bounds: {GuessGame.lower_bound} and {GuessGame.upper_bound}.')
        else:
            GuessGame.lower_bound = lower
            GuessGame.upper_bound = upper

        await ctx.send(f'You entered bounds: {GuessGame.lower_bound} and {GuessGame.upper_bound}')


    # Starting the game...
    @command(
        brief="Type `.start` to start the game.",
        description = "Type `.start` to get more details on how play the game."
    )
    async def start(self, ctx):
        await ctx.send(f'Try to guess a random number between {GuessGame.lower_bound}-{GuessGame.upper_bound}.\nType a number after `.guess` command.\nGood Luck!', delete_after=30)


    @command(
        brief="Enter the number after `.guess` to guess the right number.",
        description = "Example: `.guess 5` and repeat until you guess it right."
    )
    async def guess(self, ctx, guess_number: int):
        lower_bound = GuessGame.lower_bound
        upper_bound = GuessGame.upper_bound

        check_number = round(random.randint(lower_bound, upper_bound))  # Get random number.
        rounds_number = round(math.log(GuessGame.upper_bound - GuessGame.lower_bound + 1,2))  # Get random number of rounds. Like 3 rounds or 3 attempts left to guess.

        count = 0

        while count < check_number:
            count += 1

            if check_number == guess_number:
                await ctx.send(f'Congratulations you did it! You entered {guess_number}.\nType `.start` to play again or use `.help` to see options.')
            elif check_number > guess_number:
                await ctx.send(f'You guessed too small!  Try again {rounds_number - count} round(s) pending.', delete_after=30)
            elif check_number < guess_number:
                await ctx.send(f'You guessed too high!  Try again. {rounds_number - count} round(s) pending.', delete_after=30)
            if count >= rounds_number:
                await ctx.send(f'Sorry! The number is {check_number}. Type `.start` to play again.')


def setup(bot: Bot) -> None:
    """Load the Guess_Game cog."""
    bot.add_cog(GuessGame(bot))


#client.run('token') to test running as a bot with this file only.
