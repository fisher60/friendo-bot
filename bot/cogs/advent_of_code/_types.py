from __future__ import annotations

from pydantic import BaseModel


class PartCompletion(BaseModel):
    """Time taken to complete the day's star."""

    star_index: int
    get_star_ts: int


class LeaderboardMember(BaseModel):
    """Member data on the leaderboard."""

    id: int
    name: str | None = "Anonymous"
    stars: int
    local_score: int
    global_score: int
    last_star_ts: int
    completion_day_level: dict[int, dict[int, PartCompletion]]


class Leaderboard(BaseModel):
    """Leaderboard data."""

    owner_id: int
    event: int
    members: dict[int, LeaderboardMember]

    @property
    def year(self) -> int:
        """Get the year the leaderboard is relevant to."""
        return self.event
