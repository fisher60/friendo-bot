import json
from bot.settings import EVENT_API_KEY


class Event:
    def __init__(self, bot):
        self.bot = bot
        # event api url
        self.event_url = "https://app.ticketmaster.com/discovery/v2/events.json?"

    async def show_events(self, artist):
        artist_find = ("-").join(artist.split(" "))
        print(artist_find)
        self.event_url = f"https://app.ticketmaster.com/discovery/v2/events.json?keyword={artist_find}&apikey={EVENT_API_KEY}"
        print(self.event_url)
        async with self.bot.session.get(self.event_url) as res:
            if res.status == 200:
                event_json = await res.json()
                return event_json
            else:
                return 0
