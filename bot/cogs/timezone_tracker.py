import logging
from collections import defaultdict
from datetime import timedelta
import typing as t

import arrow
from discord import Member
import discord
from discord.ext.commands import Cog, Context, group

from bot.bot import Friendo


log = logging.getLogger(__name__)


class TimeZoneTracker(Cog):
    """A command that randomizes the cases of every letter of a word or words."""

    def __init__(self, bot: Friendo) -> None:
        self.bot = bot

    @group(
        name="timezone",
        aliases=("tz",),
        invoke_without_command=True,
        brief=(
            "The main group for timezone commands.\n"
            "Use the add subcommand to add your timezone to the database.\n"
            "Use the get subcommand to get a user's stored timezone.\n"
            "Use the list subcommand to list all guild member's timezones."
        )
    )
    async def timezone_group(self, ctx: Context) -> None:
        """The main group for timezone commands."""
        pass

    @timezone_group.command(
        name="add",
        aliases=("a", "set", "s"),
        brief=(
            "Store the given timezone against the invoker.\n"
            "See the `TZ Database name` column here "
            "https://en.wikipedia.org/wiki/List_of_tz_database_time_zones "
            "for a list of supported timezones."
        )
    )
    async def add_timezone(self, ctx: Context, tz: str) -> None:
        """
        Store the given timezone against the invoker.

        See the `TZ Database name` column here https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
        for a list of supported timezones.
        """
        try:
            arrow.now(tz)
        except arrow.parser.ParserError:
            await ctx.send(
                f":x: {ctx.author.mention} {tz} is not a valid timezone!\n\n"
                "See the `TZ Database name` column here: "
                "<https://en.wikipedia.org/wiki/List_of_tz_database_time_zones>"
            )
            return

        await self._save_tz(ctx.author.id, tz)
        await ctx.send(f":+1: Successfully set your timezone to {tz}.")

    @timezone_group.command(
        name="list",
        aliases=("l",),
        brief=(
            "List the timezone and the local time for all members on record in this guild."
        )
    )
    async def list_timezone(self, ctx: Context) -> None:
        """List the timezone and the local time for members on record in this guild."""
        tzs = await self._get_tzs(ctx.guild)

        def tz_sorter(timezone_to_member_lookup: t.Tuple[str, t.List[int]]) -> timedelta:
            """Returns the UTC offset given a single lookup."""
            timezone, _ = timezone_to_member_lookup
            return arrow.now(timezone).utcoffset()

        tzs = dict(sorted(tzs.items(), key=tz_sorter))

        lines = []
        for tz, members in tzs.items():
            time = arrow.now(tz)
            lines.append(f"**{time.format('HH:mm')}** - {tz}\n")
            for member in members:
                lines.append(f"{ctx.guild.get_member(member).mention}\n")
            lines.append("\n")

        await ctx.send(
            embed=discord.Embed(
                title="Local times!",
                description="".join(lines[:-1]),  # Don't inluce the final newline char.
                colour=discord.Color(0xff7d93)
            )
        )

    @timezone_group.command(
        name="get",
        aliases=("g",),
        brief="Get the local time where it is for the given user, or yourself if no member is given."
    )
    async def get_timezone(self, ctx: Context, member: t.Optional[Member]) -> None:
        """Get the local time where it is for the given user."""
        user = member or ctx.author
        tz = await self._get_tz(user.id)
        if tz:
            await ctx.send(f"The time for {user.mention} is {arrow.now(tz).format('HH:mm:ss')}.")
        else:
            await ctx.send(f"I don't have timezone info for {user.mention}.")

    async def _save_tz(self, user_id: int, tz: str) -> None:
        """Save the given tz against the user in the Friendo API."""
        query = (
            "mutation mod_user ($user_id: String!, $tz: String!) {"
            "   modify_user(data: { discord_id: $user_id, timezone_name:$tz }) {"
            "       discord_id"
            "   }"
            "}"
        )
        # Convert to string because Fisher stores UserIDs as strings :-(
        variables = {"user_id": str(user_id), "tz": tz}
        await self.bot.graphql.request(json={"query": query, "variables": variables})

    async def _get_tz(self, user_id: int) -> t.Optional[str]:
        """Get the tz stored against the user in the Friendo API."""
        query = (
            "mutation get_user ($user_id: String!) {"
            "   user(data: { discord_id: $user_id}) {"
            "       timezone_name"
            "   }"
            "}"
        )
        # Convert to string because Fisher stores UserIDs as strings :-(
        variables = {"user_id": str(user_id)}
        resp = await self.bot.graphql.request(json={"query": query, "variables": variables})
        if resp.get('errors'):
            return None
        return resp["data"]["user"]["timezone_name"]

    async def _get_tzs(self, guild: discord.Guild) -> t.List[dict]:
        """Get all of the tzs info stored the Friendo API."""
        query = (
            "query users{"
            "   allUsers{"
            "       discord_id"
            "       timezone_name"
            "   }"
            "}"
        )
        resp = await self.bot.graphql.request(json={"query": query})
        if resp.get('errors'):
            return None

        guild_member_ids = {member.id for member in guild.members}
        tz_to_member = defaultdict(list)
        for user in resp["data"]["allUsers"]:
            if not user["discord_id"]:
                log.error(f"User found without a discord_id!\n{user}")
                continue
            if not user["timezone_name"]:
                log.info(f"User doesn't have tz listed, skipping\n{user}")
                continue
            if int(user["discord_id"]) in guild_member_ids:
                tz_to_member[user["timezone_name"]].append(int(user["discord_id"]))
        return tz_to_member


def setup(bot: Friendo) -> None:
    """Load the TimeZoneTracker cog."""
    bot.add_cog(TimeZoneTracker(bot))
