"""Bot class functionality"""

from discord.ext import commands


class Bot(commands.Bot):
    """
    Base Class for the discord bot
    """

    name = "Friendo"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.name
