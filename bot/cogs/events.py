"""Commands for using the events module"""
import logging

from discord.ext.commands import Bot, Cog, command, group
import discord
from bot.events_api import Event
import json

logger = logging.getLogger(__name__)


class Events(Cog):
    """
    Command for using the event finder
    """

    def __init__(self, bot: Bot):
        self.bot = bot
        self.this_event = Event(bot)

    @Cog.listener()
    async def on_ready(self):
        logger.info("events cog has been loaded")

    @group(
        brief=('Event command. Usage: `.events show "[*args]"`'),
        description=(
            "`.event show [keywords]` to display keyword search for related artists event\n"
        ),
    )
    async def events(self, ctx):
        pass

    @events.command()
    async def show(self, ctx, artist):
        result = await self.this_event.show_events(artist)
        event_date = ""
        event_location = ""
        event_venue = ""
        output = ""
        filter_result = ""
        try:
            if "_embedded" in result:
                filter_result = result["_embedded"]["events"]
                output = f"**Event:** \n```md\n**{filter_result[0]['name']}**```\n**Venues**\n"
                for index, event in enumerate(filter_result):
                    if event:
                        event_date = event["dates"]["start"]["localDate"]
                        event_venue = (
                            event["_embedded"]["venues"][0]
                            if "name" in event["_embedded"]["venues"][0]
                            else None
                        )

                        if event_venue:
                            event_location = f"{event_venue['city']['name']}, {event_venue['country']['name']}"
                            # added in seperate blocks, as each instance of message block
                            # can only hold 2000 characters. Also, it looks better
                            # this way :D.
                            output = output + (
                                f"```ini\n[{event_venue['name']}]\nLocation: {event_location}\nLocal-time: {event_date}\n```"
                            )

            else:
                output = "```md\nNo results found. Please try again.```"

            await ctx.send(output)

        except KeyError as err:
            await ctx.send(f"```No results found. Please try again```")


def setup(bot: Bot) -> None:
    """Load the bot cog"""
    bot.add_cog(Events(bot))
