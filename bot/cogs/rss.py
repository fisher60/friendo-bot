from datetime import timedelta
from typing import Dict, List, Optional

import arrow
import discord
import feedparser

from discord.ext import tasks
from discord.ext.commands import Bot, Cog, Context, hybrid_command

RPI_RSS_FEED_URL = "https://rpilocator.com/feed/"
RPI_RSS_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
}

NOTIF_COOLDOWN = timedelta(hours=48)


class NotifyMember:
    def __init__(self, search: str, member: discord.Member, channel: discord.TextChannel):
        self.search_term: str = search
        self.member: discord.Member = member
        self.notify_channel: discord.TextChannel = channel
        self.notified: bool = False


notifications: Dict[int, Dict[str, NotifyMember]] = {}


def data_to_ping_from_rss(search_term: str, feed_data: List[dict]) -> Optional[str]:
    now = arrow.utcnow()
    for entry in feed_data:
        time_fmt = "ddd, DD MMM YYYY HH:mm:ss"  # Time format: Mon, 01 May 2023 15:19:40 GMT
        published = arrow.get(entry["published"], time_fmt, tzinfo="UTC")

        if search_term.lower() in entry["title"].lower() and now - published <= NOTIF_COOLDOWN:
            return entry["title"]
    return None


class RSS(Cog):
    """
    RSS feed notifier.

    Current implementation is a hacky solution to get Raspberry Pi notifications ASAP

    This cog is not safe and needs to be modified before trusting arbitrary RSS feeds
    """

    def __init__(self, bot: Bot):
        self.bot = bot
        self.rss_background_task.start()

    def cog_unload(self):
        self.rss_background_task.cancel()

    @tasks.loop(seconds=10.0)
    async def rss_background_task(self):
        rss_data = feedparser.parse(await self.pull_rss_feed(RPI_RSS_FEED_URL))["entries"][:10]

        for user_id in notifications:
            user_notifs = notifications[user_id]
            for notif in user_notifs.values():
                ping_member_data = data_to_ping_from_rss(notif.search_term, rss_data)
                if ping_member_data and not notif.notified:
                    notif.notified = True
                    await notif.notify_channel.send(f"{notif.member.mention}--{ping_member_data}")

    async def pull_rss_feed(self, url: str) -> str:
        async with self.bot.session.get(url, headers=RPI_RSS_HEADERS) as response:
            return await response.text()

    @hybrid_command(
        brief="Create or delete a new RSS notification",
        aliases=("create_notification", "notification")
    )
    async def notify(self, ctx: Context, search_term: str, delete: bool = False) -> None:
        """Add a keyword to notify you on when it appears in the RSS feed"""
        if delete:
            if ctx.author.id in notifications and search_term in notifications[ctx.author.id]:
                del notifications[ctx.author.id][search_term]
                await ctx.send("Successfully deleted search term")
            else:
                await ctx.send("You do not have permission to delete this notification or it does not exist.")
            return

        if ctx.author.id not in notifications:
            notifications[ctx.author.id] = {}

        new_search = NotifyMember(search_term, ctx.author, ctx.channel)
        notifications[ctx.author.id][search_term] = new_search

        await ctx.send("Successfully added notification.")


async def setup(bot: Bot) -> None:
    """Load the RSS cog."""
    await bot.add_cog(RSS(bot))
