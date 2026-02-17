from __future__ import annotations

from enum import StrEnum

import discord


class Player(StrEnum):
    """Represents a player using notation to match chess.com urls."""

    White = "w"
    Black = "b"

    @staticmethod
    def to_colour(p: Player) -> discord.Colour:
        """Convert a player to a valid discord.py colour."""
        if p is Player.White:
            return discord.Colour.from_rgb(r=254, g=255, b=255)
        return discord.Colour.from_rgb(r=1, g=0, b=0)


class Piece(StrEnum):
    """Represents a piece using notation to match chess.com urls."""

    Pawn = "p"
    Knight = "n"
    Bishop = "b"
    Rook = "r"
    Queen = "q"
    King = "k"

    @staticmethod
    def to_url(piece: Piece, player: Player) -> str:
        """Convert a piece and player to a chess.com icon."""
        return f"https://www.chess.com/chess-themes/pieces/neo/150/{player.value}{piece.value}.png"
