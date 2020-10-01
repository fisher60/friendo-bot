"""Commands for using the events module"""
from discord.ext.commands import Bot, Cog, command, group
import discord
import requests
import os
import json

# constants for the api
API_KEY = os.environ.get("EVENT_API_KEY")


class Events(Cog):
    """
    Command for using the event finder
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("events cog has been loaded")

    @group()
    async def events(self, ctx):
        await ctx.send("Events:")

    @events.command()
    async def venue(self, ctx, artist):
        details = requests.get(
            f"https://app.ticketmaster.com/discovery/v2/events.json?size=1&keyword={artist}&apikey={API_KEY}"
        )
        events = dict()
        details_json = details.json()
        for event in details_json["_embedded"]["events"]:
            print(event["name"])
        # print(json.dumps(details.json(), indent=2))
        print(details.status_code)
        await ctx.send(f"Showing event venues for {artist}:")


def setup(bot: Bot) -> None:
    """Load the bot cog"""
    bot.add_cog(Events(bot))
