import discord
import math, random
from discord.ext.commands import Bot, Cog, command


class GuessGame(Cog): #(Cog): # Include Cog if it's a part of Cog file in Friendo Bot. Change class name if needed.
    """Commands for Guessing Right Number"""

    def __init__(self, bot: Bot):
        self.bot = bot

    # Variables in class GuessGame
    #Default bounds, random number, and rounds.
    lower_bound = 1
    upper_bound = 10

    check_number = round(random.randint(lower_bound, upper_bound))
    rounds_number = round(math.log(upper_bound - lower_bound + 1,
                                   2))

    # Look in `guess` command below.
    count = 0

    ### Commands
    @command(
        brief="- 1-10 Bound is Default. See `.help bound` for more details.",
        description = " - `.bound n1 n2`\nn1 => lower_bound, n2 => upper_bound\n Example: `.bound 1 10` will set the bound to 1 and 10.\nTo make Bound: 1-10 default, please type `.reset` to restart the bot."
    )

    # Set up the bounds.  Optional.  (1,10) is the default.
    async def bound(self, ctx, lower: int,upper: int):
        if lower < upper:
            # Change default bounds
            GuessGame.lower_bound = lower
            GuessGame.upper_bound = upper

            # Get new random number and rounds.
            GuessGame.check_number = round(random.randint(GuessGame.lower_bound, GuessGame.upper_bound))  # Get random number.
            GuessGame.rounds_number = round(math.log(GuessGame.upper_bound - GuessGame.lower_bound + 1,2))  # Get random number of rounds.

            await ctx.send(f'You entered bounds: {GuessGame.lower_bound} and {GuessGame.upper_bound}\nPlease `.start` or `.guess n`', delete_after=40)

        elif lower >= upper:
            await ctx.send(f'Sorry! The bound is wrong. Try again.', delete_after=30)

    # Starting the game...
    @command(
        brief=" - Type `.start` to start the game.",
        description = " - Type `.start` to get more details on how play the game."
    )
    async def start(self, ctx):
        await ctx.send(f'Try to guess a random number between {GuessGame.lower_bound}-{GuessGame.upper_bound}.\nType a number after `.guess` command.\nGood Luck!', delete_after=30)

    # Testing the guess number...
    @command(
        brief=" - Enter the number after `.guess` to guess the right number.",
        description = " - Example: `.guess 5` and repeat until you guess it right."
    )
    async def guess(self, ctx, guess_number: int):
        await ctx.send(f'Bounds: {GuessGame.lower_bound}, {GuessGame.upper_bound}', delete_after=30) #To see if bounds are set properly. Keeping it since it's useful for users to see their bounds.

        check_number = GuessGame.check_number
        rounds_number = GuessGame.rounds_number

        GuessGame.count += 1

        if check_number == guess_number:
            await ctx.send(f'Congratulations you did it! You entered {guess_number}.\nPlease enter `.reset` to restart the bot. Type `.start` to play again or use `.help` to see options.')
            GuessGame.count -= rounds_number # So we don't bother passing `4th` if statement.
        elif check_number > guess_number:
            await ctx.send(f'You guessed too small!  Try again {rounds_number - GuessGame.count} round(s) pending.', delete_after=30)
        elif check_number < guess_number:
            await ctx.send(f'You guessed too high!  Try again. {rounds_number - GuessGame.count} round(s) pending.', delete_after=30)
        if GuessGame.count >= rounds_number:
            await ctx.send(f'Sorry! The number is {check_number}. Please enter `.reset` to restart the bot. Type `.start` to play again.')


    # Restart the bot. (Not really)
    @command(
        brief=" - Restart the bot.",
        description=" - Make everything default."
    )
    async def reset(self, ctx):
        # Make everything default.
        GuessGame.lower_bound = 1
        GuessGame.upper_bound = 10

        GuessGame.check_number = round(random.randint(GuessGame.lower_bound, GuessGame.upper_bound))
        GuessGame.rounds_number = round(math.log(GuessGame.upper_bound - GuessGame.lower_bound + 1,
                                       2))

        GuessGame.count = 0

        await ctx.send(f'Thank you for restarting.  Please `.start` to play again or use `.help` to see options.')

def setup(bot: Bot) -> None:
    """Load the Guess_Game cog."""
    bot.add_cog(GuessGame(bot))

#client.run('token')
