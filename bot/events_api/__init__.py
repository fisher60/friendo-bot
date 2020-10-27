import logging
from typing import Any, Dict, Optional

from bot.bot import Friendo
from bot.settings import EVENT_API_KEY

logger = logging.getLogger(__name__)

EVENT_URL = "https://app.ticketmaster.com/discovery/v2/events.json?"


class Event:
    """An event for the event API."""

    def __init__(self, bot: Friendo) -> None:
        self.bot = bot

    async def show_events(self, artist: str) -> Optional[Dict[Any]]:
        """Show an event by requesting from it's webpage."""
        artist_find = "-".join(artist.split(" "))

        event_url = f"{EVENT_URL}keyword={artist_find}&apikey={EVENT_API_KEY}"

        async with self.bot.session.get(event_url) as res:
            if res.status == 200:
                event_json = await res.json()
                return event_json
