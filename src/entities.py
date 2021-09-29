from dataclasses import dataclass
from enum import Enum


class MatchPhase(Enum):
    HALFTIME: "halftime"
    FULLTIME: "fulltime"
    EXTRATIME: "extratime"
    PENALTIES: "penalty"


@dataclass
class MatchScore:
    home_score: int
    away_score: int


@dataclass
class Fixture:
    date: str
    referee: str
    match_status: str
    championship: str
    round: str
    home_team: str
    away_team: str
    # scores: Dict[str, MatchScore]

    def __str__(self):
        return f"Date (UTC): {self.date}\n\n" \
               f"Match: {self.home_team} vs. {self.away_team}\n" \
               f"Championship: {self.championship}\n" \
               f"Round: {self.round}\n" \
               f"Referee: {self.referee}\n" \
               f"Status: {self.match_status}\n"
