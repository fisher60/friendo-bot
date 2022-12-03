import logging
from datetime import datetime
from itertools import cycle
from operator import attrgetter

import discord
from discord import app_commands, Embed, Color
from discord.ext import commands

from bot.bot import Friendo
from bot.settings import AOC_JOIN_CODE, AOC_SESSION_COOKIE, AOC_LEADERBOARD_ID
from ._types import Leaderboard, LeaderboardMember

logger = logging.getLogger("advent_of_code")


class AdventOfCode(commands.GroupCog):
    """Commands for Advent of Code."""

    def __init__(self, bot: Friendo):
        self.bot = bot
        super().__init__()

    async def fetch_leaderboard(self, year: int) -> Leaderboard:
        """Get the leaderboard's state for a specified year."""
        url = f"https://adventofcode.com/{year}/leaderboard/private/view/{AOC_LEADERBOARD_ID}.json"
        cookies = {'session': AOC_SESSION_COOKIE}

        # AoC Author has requested applications to provide a url to the tool in the User-Agent
        headers = {'User-Agent': 'github.com/fisher60/friendo-bot'}

        async with self.bot.session.get(url, cookies=cookies, headers=headers) as response:
            data = await response.json()
            return Leaderboard(**data)

    @staticmethod
    def _create_leaderboard_message(members: list[LeaderboardMember], amount: int) -> str:
        reset = "[0m"
        red = "[1;31m"
        green = "[1;32m"
        yellow = "[1;33m"

        get_line_color = cycle([red, green])

        formatted_message = f"Here is our top {amount}\n```ansi\n"
        for rank, member in enumerate(members[:amount], start=1):
            formatted_message += (
                f"{next(get_line_color)}{rank:0>2} {yellow}★{reset} {member.name} ({member.local_score})\n"
            )

        formatted_message += "```"

        return formatted_message

    @app_commands.command()
    @app_commands.describe(
        year="View the leaderboard from a specific year, defaults to the current year",
        amount="How many members to view, defaults to 10"
    )
    async def leaderboard(
            self,
            interaction: discord.Interaction,
            year: app_commands.Range[int, 2015, None] = None,
            amount: app_commands.Range[int, 0, None] = 10
    ) -> None:
        """ Get the current Advent of Code leaderboard """
        if year is None:
            year = datetime.now().year
        elif year > datetime.now().year:  # Don't allow years that haven't happened yet
            await interaction.response.send_message(
                f"> Please select a valid year 2015 - {datetime.now().year}",
                ephemeral=True
            )
            return

        leaderboard = await self.fetch_leaderboard(year)

        all_member = list(filter(attrgetter("local_score"), leaderboard.members.values()))
        all_member.sort(key=attrgetter("local_score"), reverse=True)

        embed = Embed(
            title=f"Advent of Code {leaderboard.year}",
            description=self._create_leaderboard_message(all_member, amount),
            url="https://adventofcode.com",
            colour=Color.gold(),
        )
        embed.add_field(
            name="\u200b",
            value="Join the fun with `/advent-of-code join`"
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def join(self, interaction: discord.Interaction) -> None:
        """Find out how to join the Advent of Code leaderboard!"""
        await interaction.response.send_message(
            ">>> To join the leaderboard, follow these steps:\n"
            "\t1. Log in on https://adventofcode.com\n"
            "\t2. Head over to https://adventofcode.com/leaderboard/private\n"
            f"\t3. Use this code `{AOC_JOIN_CODE}`",
            ephemeral=True
        )
