import random
from pathlib import Path

import yaml
from discord.ext.commands import Bot, Cog, Context, command

with open(Path.cwd() / 'bot' / 'resources' / 'greetings.yaml', 'r', encoding='utf-8') as f:
    info = yaml.load(f, Loader=yaml.FullLoader)
    PRAISE, ROAST = info['praise'], info['roast']


class Greetings(Cog):
    """Simple ask-reply commands, good for testing or making members feel welcome."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(brief="Say hello", aliases=["hi", "ello", "howdy", "hola"])
    async def hello(self, ctx: Context) -> None:
        """Greets a user, with a variety of options."""
        msgs = [
            f"Hello There! {ctx.author.mention} 🖐",
            f"Hi! {random.choice(PRAISE)} {ctx.author.mention}",
            f"What's Up {random.choice(PRAISE)} {ctx.author.mention}!",
            f"Howdy fellow member, How ya doin {ctx.author.mention}",
            f"G'day Mate! {ctx.author.mention}, Woof Woof!",
            f"Good to see you! {random.choice(PRAISE)} {ctx.author.mention}",
            f"Hmm, hello {random.choice(ROAST)} {ctx.author.mention}, LOL",
        ]

        await ctx.send(random.choice(msgs))


async def setup(bot: Bot) -> None:
    """Load the Greetings cog."""
    await bot.add_cog(Greetings(bot))
