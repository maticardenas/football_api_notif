from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List

from src.emojis import Emojis


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
class Team:
    id: str
    name: str
    picture: str


@dataclass
class Championship:
    league_id: int
    name: str
    country: str
    logo: str


@dataclass
class MatchHighlights:
    url: str
    embed_url: str


@dataclass
class RemainingTime:
    days: int
    hours: int
    minutes: int

    def __str__(self):
        suf_faltan = "n" if self.days != 1 else ""
        suf_dias = "s" if self.days != 1 else ""
        suf_horas = "s" if self.hours != 1 else ""
        suf_minutos = "s" if self.minutes != 1 else ""

        days_phrase = f"{self.days} día{suf_dias}, " if self.days > 0 else ""
        hours_phrase = f"{self.hours} hora{suf_horas} y " if self.hours > 0 else ""

        return f"Falta{suf_faltan} {days_phrase}{hours_phrase}{self.minutes} minuto{suf_minutos}"


@dataclass
class Fixture:
    utc_date: datetime
    ams_date: datetime
    bsas_date: datetime
    date_diff: int
    referee: str
    match_status: str
    championship: Championship
    round: str
    home_team: Team
    away_team: Team
    match_score: MatchScore
    is_next_day: str = field(init=False)
    highlights: List[MatchHighlights] = field(init=False)

    def __post_init__(self) -> None:
        self.is_next_day = "(+1)" if self._is_next_day_in_europe() else ""

    def remaining_time(self) -> RemainingTime:
        days = self.date_diff // 86400
        hours = (self.date_diff - (days * 86400)) // 3600
        minutes = (self.date_diff - (days * 86400) - (hours * 3600)) // 60

        return RemainingTime(days, hours, minutes)

    def __str__(self):
        return (
            f"{Emojis.EUROPEAN_UNION.value} *{str(self.ams_date)[11:16]} HS {self.is_next_day}*\n"
            f"{Emojis.ARGENTINA.value} *{str(self.bsas_date)[11:16]} HS*\n\n"
            f"{Emojis.ALARM_CLOCK.value} _{str(self.remaining_time())} para el partido._\n\n"
            f"{Emojis.SOCCER_BALL.value} *{self.home_team.name} vs. {self.away_team.name}*\n"
            f"{Emojis.TROPHY.value} *{self.championship.name}*\n"
            f"{Emojis.PUSHPIN.value} *{self.round}*"
        )

    def matched_played_str(self) -> str:
        return (
            f"{Emojis.SOCCER_BALL.value} *{self.home_team.name} - {self.match_score.home_score} "
            f"vs. {self.match_score.away_score} - {self.away_team.name}*\n"
            f"{Emojis.TROPHY.value} *{self.championship.name}*\n"
            f"{Emojis.PUSHPIN.value} *{self.round}*"
        )

    def email_like_repr(self) -> str:
        return (
            f"<p>{Emojis.EUROPEAN_UNION.value} <strong>{str(self.ams_date)[11:16]} HS {self.is_next_day}<br />"
            f"{Emojis.ARGENTINA.value} <strong>{str(self.bsas_date)[11:16]} HS</strong><p>"
            f"{Emojis.ALARM_CLOCK.value} <em>{str(self.remaining_time())} para el partido.</em><p>"
            f"{Emojis.SOCCER_BALL.value} "
            f"<img src='{self.home_team.picture}' width='22' height='22'><strong> vs. "
            f"<img src='{self.away_team.picture}' width='22' height='22'></strong><br />"
            f"<img src='{self.championship.logo}' width='22' height='22'> <strong>{self.championship.name}</strong><br />"
            f"{Emojis.PUSHPIN.value} <strong>{self.round}</strong>"
        )

    def matched_played_email_like_repr(self) -> str:
        return (
            f"<p><img src='{self.home_team.picture}' width='22' height='22'><strong> - {self.match_score.home_score} vs. "
            f" {self.match_score.away_score} - <img src='{self.away_team.picture}' width='22' height='22'></strong><br />"
            f"<img src='{self.championship.logo}' width='25' height='25'> <strong>{self.championship.name}</strong><br />"
            f"{Emojis.PUSHPIN.value} <strong>{self.round}</strong>"
        )

    def _is_next_day_in_europe(self) -> bool:
        return self.bsas_date.weekday() != self.ams_date.weekday()


@dataclass
class TeamStanding:
    championship: Championship
    position: int
    points: int
    goal_difference: int
    current_condition: str

    def __str__(self):
        return (
            f"{Emojis.CHART_INCREASING.value} Posición: *{self.position}*\n"
            f"{Emojis.CHECK_MARK.value} Puntos: *{self.points}*\n"
            f"{Emojis.GOAL_NET.value} Diferencia de gol: *{self.goal_difference}*\n"
            f"{Emojis.GLOBE_WITH_MERIDIANS.value} Clasificación: *{self.current_condition}*"
        )

    def email_like_repr(self) -> str:
        return (
            f"<br /><br />{Emojis.CHART_INCREASING.value} Posición: <strong>{self.position}</strong><br />"
            f"{Emojis.CHECK_MARK.value} Puntos: <strong>{self.points}</strong><br />"
            f"{Emojis.GOAL_NET.value} Diferencia de gol: <strong>{self.goal_difference}</strong><br />"
            f"{Emojis.GLOBE_WITH_MERIDIANS.value} Clasificación: <strong>{self.current_condition}</strong>"
        )


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
        return (
            f"_Appearances:_ *{self.appearences}*\n"
            f"_Goals:_ *{self.goals}*\n"
            f"_Minutes:_ *{self.minutes}*\n"
            f"_Total Shots:_ *{self.total_shots}*\n"
            f"_Shots on target:_ *{self.shots_on_target}*\n\n"
            f"_Total Passes:_ *{self.total_passes}*\n"
            f"_Key Passes:_ *{self.key_passes}*\n"
            f"_Accuracy:_ *{self.accuracy}*\n\n"
            f"_Dribbles Attempts:_ *{self.dribbles_attempts}*\n"
            f"_Dribbles Success:_ *{self.dribbles_success}*"
        )
