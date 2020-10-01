"""Commands for using the events module"""
from discord.ext.commands import Bot, Cog, command, group
import discord
from bot.events_api import Event
import json


class Events(Cog):
    """
    Command for using the event finder
    """

    def __init__(self, bot: Bot):
        self.bot = bot
        self.this_event = Event(bot)

    @Cog.listener()
    async def on_ready(self):
        print("events cog has been loaded")

    @group()
    async def events(self, ctx):
        await ctx.send("Events:")

    @events.command()
    async def show(self, ctx, artist):
        result = await self.this_event.show_events(artist)
        for event in result:
            if event:
                name = (
                    event["_embedded"]["venues"][0]["name"]
                    if "name" in event["_embedded"]["venues"][0]
                    else None
                )
                if name:
                    await ctx.send(name)


def setup(bot: Bot) -> None:
    """Load the bot cog"""
    bot.add_cog(Events(bot))
