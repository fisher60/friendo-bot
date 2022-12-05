import logging

import discord
from discord import Color, Embed, app_commands
from discord.ext import commands
from discord.utils import snowflake_time

from bot.bot import Friendo

logger = logging.getLogger("convert")


class Convert(commands.GroupCog):
    """Commands for Conversions."""

    def __init__(self, bot: Friendo):
        self.bot = bot
        super().__init__()

    @app_commands.command()
    @app_commands.describe(
        snowflake="Snowflake to convert to a timestamp",
        ephemeral="Should output only be shown to you?",
    )
    async def snowflake_to_timestamp(
            self,
            interaction: discord.Interaction,
            snowflake: str,
            ephemeral: bool = True
    ) -> None:
        """Convert a discord snowflake to a timestamp."""
        try:
            if len(snowflake) < 17:
                raise ValueError("Snowflake is too small to be valid")

            snowflake = int(snowflake)
        except ValueError:
            await interaction.response.send_message(
                "> Provided input was not a valid snowflake.",
                ephemeral=ephemeral
            )
            return

        snowflake_timestamp = round(snowflake_time(snowflake).timestamp())
        await interaction.response.send_message(
            f"> Snowflake `{snowflake}` was <t:{snowflake_timestamp}:R>",
            ephemeral=True
        )

    @app_commands.command()
    @app_commands.describe(
        color="Color to attempt to convert, e.g. #<hex>, rgb(<red>,<green>,<blue>)",
        ephemeral="Should output only be shown to you?",
    )
    async def color(self, interaction: discord.Interaction, color: str, ephemeral: bool = True) -> None:
        """Get conversion information for a color -- Decimal, Hexadecimal and RGB."""
        try:
            color = Color.from_str(color)
        except ValueError:
            await interaction.response.send_message(
                ">>> Unable to understand that color format. Please try one of the following examples.\n"
                "\t- `rgb(17, 32, 115)`\n"
                "\t- `#F3AAC7`\n",
                ephemeral=True
            )
            return

        embed = Embed(
            title="Color",
            color=color,
        )
        embed.add_field(name="RGB", value=f"`({color.r},{color.g},{color.b})`")
        embed.add_field(name="Hexadecimal", value=f"`#{color.value:0X}`")
        embed.add_field(name="Decimal", value=f"`{color.value}`")

        await interaction.response.send_message(
            embed=embed,
            ephemeral=ephemeral
        )
