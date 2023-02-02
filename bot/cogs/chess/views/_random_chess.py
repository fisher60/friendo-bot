import random

import discord

from .._types import Piece, Player


class RandomChess(discord.ui.View):
    """RandomChess view, gives you random pieces to play each turn."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_player = Player.White
        self.turn_number = 1
        self.available_moves = list(Piece)
        self.current_move = Piece.Pawn
        self.select_random_move()

    def select_random_move(self) -> None:
        """Select a random move from the available moves list, if empty repopulate the list."""
        if len(self.available_moves) == 0:
            list(Piece)

        self.current_move = random.choice(self.available_moves)
        self.available_moves.remove(self.current_move)

    @discord.ui.button(label='Next Move', style=discord.ButtonStyle.success)
    async def next_move(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        """Next move button handler."""
        if self.current_player is Player.Black:
            self.turn_number += 1

        self.current_player = Player.White if self.current_player is Player.Black else Player.Black
        self.available_moves = list(Piece)
        self.select_random_move()

        await interaction.response.defer()
        await interaction.message.edit(embed=self.generate_embed(), view=self)

    @discord.ui.button(label='Invalid Move', style=discord.ButtonStyle.danger)
    async def invalid_move(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        """Invalid move button handler."""
        self.select_random_move()
        await interaction.response.defer()
        await interaction.message.edit(embed=self.generate_embed(), view=self)

    def generate_embed(self) -> discord.Embed:
        """Generate an embed to represent the current state of the view."""
        embed = discord.Embed(
            title="Random Chess",
            description=f"{self.current_player.name} to move",
            colour=Player.to_colour(self.current_player),
        )

        embed.add_field(name="Turn", value=self.turn_number)
        embed.add_field(name="Piece", value=self.current_move.name)
        embed.set_thumbnail(url=Piece.to_url(self.current_move, self.current_player))
        return embed
