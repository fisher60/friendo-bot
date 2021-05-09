import json
import logging
from pathlib import Path
import re
from typing import Callable, Optional

from discord import Member
from discord.ext.commands import Cog, Context, check, command

from bot.bot import Friendo

log = logging.getLogger(__name__)


def is_bot_admin() -> Callable:
    """Return whether or not the user invoking a command is an bot admin."""

    def predicate(ctx: Context) -> bool:
        """Opening the admin json config file."""
        with open(Path.cwd() / "bot" / "save_data.JSON", "r") as file:
            save_data = json.load(file)

        return str(ctx.message.author.id) in save_data["admins"]

    return check(predicate)


def id_from_mention(message_content: str) -> Optional[int]:
    """Return a user id from an @mention in a message."""
    get_id = re.search(r"\d{18}", message_content)

    if get_id is not None:
        return int(get_id.group())


class Administration(Cog):
    """Commands for bot and server administration, all require the admin status on the invoking user."""

    def __init__(self, bot: Friendo) -> None:
        self.bot = bot

    @command(brief="Kills your robotic friend")
    @is_bot_admin()
    async def shutdown(self, ctx: Context) -> None:
        """Cleanly shuts down the bot."""
        await ctx.send("Mr. Stark, I don't feel so good...")

        log.info("Closing Client...")

        await self.bot.logout()

    @command(name="createadmin", brief="gives the @mention user admin permissions")
    @is_bot_admin()
    async def create_admin(self, ctx: Context, member: Member) -> None:
        """Adds a new user id to the list of admins."""
        msg = f"Could not create admin from {member.name}"

        with open(Path.cwd() / "save_data.json", "r") as file:
            save_data = json.load(file)

        if str(member.id) not in save_data["admins"]:
            save_data["admins"].append(str(member.id))

            with open(Path.cwd() / "save_data.json", "r") as file:
                json.dump(save_data, file)
                msg = f"{ctx.author.mention}, {member.name} has been added to admins"

        await ctx.send(msg)


def setup(bot: Friendo) -> None:
    """Load the Admin cog."""
    bot.add_cog(Administration(bot))
