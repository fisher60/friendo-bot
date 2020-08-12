import discord
from discord.ext import commands


class Bot(commands.bot):
    name = "Friendo"

    def __str__(self):
        return self.name
