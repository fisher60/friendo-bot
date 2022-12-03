from __future__ import annotations

from pydantic import BaseModel


class PartCompletion(BaseModel):
    star_index: int
    get_star_ts: int


class LeaderboardMember(BaseModel):
    id: int
    name: str
    stars: int
    local_score: int
    global_score: int
    last_star_ts: int
    completion_day_level: dict[int, dict[int, PartCompletion]]


class Leaderboard(BaseModel):
    owner_id: int
    event: int
    members: dict[int, LeaderboardMember]

    @property
    def year(self) -> int:
        return self.event
