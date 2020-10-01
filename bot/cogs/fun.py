"""
Commands that do not serve a useful function aside from being fun.
"""

from random import choice
from discord import Embed, Colour
from discord.ext.commands import Bot, Cog, command


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
        """Converts input string to alternating case."""
        count = 0
        new = ""
        for i in phrase.lower():
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
        description="accepts a string value of heads or tails and tells you if you win or lose the call, ie .flip heads",
        name="flip",
    )
    async def coin_toss(self, ctx, toss):
        """Determines whether or not a user won a coin toss."""

        outcomes = ["heads", "tails"]

        if toss == choice(outcomes):
            msg = f"{ctx.author.mention} wins!"
        else:
            msg = f"{ctx.author.mention} loses!"

        await ctx.send(msg)

    @command(
        brief="Ask any question to the 8ball",
        description="accepts a question and gives you an 8ball answer",
        name="8ball",
    )
    async def eight_ball(self, ctx, *, question=None):
        """Returns an 8ball response to a user's question."""

        responses = [
            "It is certain",
            "Yes, definately",
            "Without a doubt",
            "Thats for sure",
            "Most likely",
            "Umm, try again",
            "Didnt quite get that",
            "Concentrate and try again",
            "Not likely at all",
            "My reply is no",
            "Obviously not",
            "No...",
            "My sources say no",
        ]

        if question:
            await ctx.send(f"Question: {question}\nAnswer: {choice(responses)}")

        # Send help if question == None
        else:
            embed = Embed(
                title="8ball",
                colour=Colour.blue(),
                description="Usage: `.8ball will this command work?`",
            )
            await ctx.send(embed=embed)
            
    @command(
        brief="Play a game of rock paper scissors",
        description="Enter an option between rock, paper, scissor after .play",
        aliases= ["play", "Play", "RPS"],
    )
    async def rps(self, ctx, *, response=None):
        """Returns strings based on winning/losing/tie"""
        response = response.lower()
        options = ['rock', 'paper', 'scissors']
        bot_choice = random.choice(options)
        win = ctx.send("I win... I hope you arent angry?.😂")
        lose = ctx.send("I lose.. 😶")
        choose = ctx.send(f'I choose {bot_choice}')
        
        if response not in options:
            await ctx.send("Please choose between rock, paper or scissors")
        elif response == bot_choice:
            await ctx.send(f"I choose {bot_choice}\nOh, we got a tie")
            
        elif response == 'rock':
            await choose
            await (win) if bot_choice == 'paper' else await (lose)   
            
        elif response == 'paper':
            await choose
            await (win) if bot_choice == 'scissors' else await (lose)   
       
        elif response == 'scissors':
            await choose
            await (win) if bot_choice == 'rock' else await (lose)
        # I forgot to do this last time sorry
        else:
            embed = Embed(
                title="Rock, Paper, Scissor",
                colour=Colour.red(),
                description="Usage: `.rps rock/paper/scissors`",
            )
            await ctx.send(embed=embed)


def setup(bot: Bot) -> None:
    """Load the Fun cog."""
    bot.add_cog(Fun(bot))
