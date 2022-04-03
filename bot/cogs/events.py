from disnake.ext.commands import Cog, Context, group

from bot.bot import Friendo
from bot.events_api import Event


class Events(Cog):
    """Command(s) for using the event API."""

    def __init__(self, bot: Friendo) -> None:
        self.bot = bot
        self.this_event = Event(bot)

    @group(brief='Event command. Usage: `.events show "[*args]"`',
           description="`.event show [keywords]` to display keyword search for related artists event\n",
           )
    async def events(self, ctx: Context) -> None:
        """Group commands for events."""
        pass

    @events.command()
    async def show(self, ctx: Context, artist: str) -> None:
        """Showing an event."""
        result = await self.this_event.show_events(artist)

        try:
            if "_embedded" in result:
                filter_result = result["_embedded"]["events"]
                output = f"**Event:** \n```md\n**{filter_result[0]['name']}**```\n**Venues**\n"

                for event in filter_result:
                    if event:
                        event_date = event["dates"]["start"]["localDate"]
                        event_venue = (
                            event["_embedded"]["venues"][0]
                            if "name" in event["_embedded"]["venues"][0]
                            else None
                        )

                        if event_venue:
                            e_location = f"{event_venue['city']['name']}, {event_venue['country']['name']}"

                            output = output + ((
                                f"```ini\n[{event_venue['name']}]\n```"
                                f"Location: {e_location}\nLocal-time: {event_date}"
                            ))

            else:
                output = "```md\nNo results found. Please try again.```"

            await ctx.send(output)

        except KeyError:
            await ctx.send("```\nNo results found. Please try again```")


def setup(bot: Friendo) -> None:
    """Load the events cog."""
    bot.add_cog(Events(bot))
