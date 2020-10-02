"""Commands that greet users, meant as an example/base for writing new cogs."""
import random
from discord.ext.commands import Bot, Cog, command

class Greetings(Cog):
    """Simple ask-reply commands, good for testing or making members feel welcome."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(brief="Say hello", aliases=["hi", "ello", "howdy", "hola"])
    async def hello(self, ctx):
        """Tells a user 'hello'"""
        praise = ["Lovely", "Beautiful", "Smart", "Naughty", "Friendly", "Helpful", "Charming", "Courageous","Affectionate", "Generous", "Reliable", "Witty"]
                  
        roast = ["Arrogant", "Bossy", "Boastful", "Unreliable", "Careless", "Ugly (a little)"]
        
        msgs = [    
            f"Hello There! {ctx.author.mention} 🖐", f"Hi! {random.choice(praise)} {ctx.author.mention}",
            f"What's Up {random.choice(praise)} {ctx.author.mention}!", f"Howdy fellow member, How ya doin {ctx.author.mention}",
            f"G'day Mate! {ctx.author.mention}, Woof Woof!", f"Good to see you! {random.choice(praise)} {ctx.author.mention}",
            f"Hmm, hello {random.choice(roast)} {ctx.author.mention}, LOL"]
        
        await ctx.send(random.choice(msgs))
        


def setup(bot: Bot) -> None:
    """Load the Greetings cog."""
    bot.add_cog(Greetings(bot))
