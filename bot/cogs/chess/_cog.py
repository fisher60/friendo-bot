from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from .views._random_chess import RandomChess

if TYPE_CHECKING:
    from bot.bot import Friendo


class Chess(commands.GroupCog):
    """Commands related to chess."""

    def __init__(self, bot: Friendo):
        self.bot = bot
        super().__init__()

    @app_commands.command()
    async def random_chess(self, interaction: discord.Interaction) -> None:
        """Get prompts to play random chess."""
        chess_view = RandomChess()
        await interaction.response.send_message(embed=chess_view.generate_embed(), view=chess_view)
