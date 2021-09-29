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

@dataclass
class Championship:
    name: str
    country: str


@dataclass
class Team:
    name: str
    country: str


@dataclass
class Player:
    name: str
    age: str
    nationality: str
    team: str
    height: str
    weight: str


@dataclass
class PlayerStats:
    appearences: int
    minutes: int
    total_shots: int
    shots_on_target: int
    goals: int
    total_passes: int
    key_passes: int
    accuracy: int
    dribbles_attempts: int
    dribbles_success: int

    def __str__(self):
        return f"Appearances: {self.appearences}\n" \
               f"Goals: {self.goals}\n" \
               f"Minutes: {self.minutes}\n" \
               f"Total Shots: {self.total_shots}\n" \
               f"Shots on target: {self.shots_on_target}\n\n" \
               f"Total Passes: {self.total_passes}\n" \
               f"Key Passes: {self.key_passes}\n" \
               f"Accuracy: {self.accuracy}\n\n" \
               f"Dribbles Attempts: {self.dribbles_attempts}\n" \
               f"Dribbles Success: {self.dribbles_success}"

