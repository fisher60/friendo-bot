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
        pass

    @events.command()
    async def show(self, ctx, artist):
        result = await self.this_event.show_events(artist)
        output = f"**Event:** \n```md\n**{result[0]['name']}**```\n**Venues**\n"
        for event in result:
            if event:
                event_date = event["dates"]["start"]["localDate"]
                event_venue = (
                    event["_embedded"]["venues"][0]
                    if "name" in event["_embedded"]["venues"][0]
                    else None
                )
                if event_venue:
                    output = (
                        output
                        + (
                            f"```ini\n[{event_venue['name']}]\nLocation: {event_venue['city']['name']}\nLocal-time: {event_date}```"
                        )
                        + "\n"
                    )
        # output += "```"
        await ctx.send(output)


def setup(bot: Bot) -> None:
    """Load the bot cog"""
    bot.add_cog(Events(bot))
