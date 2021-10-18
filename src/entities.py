from dataclasses import dataclass
from datetime import datetime
from enum import Enum

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
class RemainingTime:
    days: int
    hours: int
    minutes: int

    def __str__(self):
        suf_faltan = "n" if self.days != 1 else ""
        suf_dias = "s" if self.days != 1 else ""
        suf_horas = "s" if self.hours != 1 else ""
        suf_minutos = "s" if self.minutes != 1 else ""

        return f"Falta{suf_faltan} {self.days} día{suf_dias}, {self.hours} " \
               f"hora{suf_horas} y {self.minutes} minuto{suf_minutos}"

@dataclass
class Fixture:
    utc_date: datetime
    ams_date: str
    bsas_date: str
    date_diff: int
    referee: str
    match_status: str
    championship: str
    round: str
    home_team: str
    away_team: str

    def remaining_time(self) -> RemainingTime:
        days = self.date_diff//86400
        hours = (self.date_diff - (days * 86400)) // 3600
        minutes = (self.date_diff - (days * 86400) - (hours * 3600)) // 60

        return RemainingTime(
            days,
            hours,
            minutes
        )

    def __str__(self):
        return f"{Emojis.EUROPEAN_UNION.value} *{self.ams_date[11:16]} HS*\n" \
               f"{Emojis.ARGENTINA.value} *{self.bsas_date[11:16]} HS*\n\n" \
               f"{Emojis.ALARM_CLOCK.value} _{str(self.remaining_time())} para el partido._\n\n" \
               f"{Emojis.SOCCER_BALL.value} *{self.home_team} vs. {self.away_team}*\n" \
               f"{Emojis.TROPHY.value} *{self.championship}*\n" \
               f"{Emojis.PUSHPIN.value} *{self.round}*"

    def email_like_repr(self) -> str:
         return f"<p>{Emojis.EUROPEAN_UNION.value} <strong>{self.ams_date[11:16]} HS<br />" \
               f"{Emojis.ARGENTINA.value} <strong>{self.bsas_date[11:16]} HS</strong><p>" \
               f"{Emojis.ALARM_CLOCK.value} <em>{str(self.remaining_time())} para el partido.</em><p>" \
               f"{Emojis.SOCCER_BALL.value} <strong>{self.home_team} vs. {self.away_team}</strong><br />" \
               f"{Emojis.TROPHY.value} <strong>{self.championship}</strong><br />" \
               f"{Emojis.PUSHPIN.value} <strong>{self.round}</strong>"



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
        return f"_Appearances:_ *{self.appearences}*\n" \
               f"_Goals:_ *{self.goals}*\n" \
               f"_Minutes:_ *{self.minutes}*\n" \
               f"_Total Shots:_ *{self.total_shots}*\n" \
               f"_Shots on target:_ *{self.shots_on_target}*\n\n" \
               f"_Total Passes:_ *{self.total_passes}*\n" \
               f"_Key Passes:_ *{self.key_passes}*\n" \
               f"_Accuracy:_ *{self.accuracy}*\n\n" \
               f"_Dribbles Attempts:_ *{self.dribbles_attempts}*\n" \
               f"_Dribbles Success:_ *{self.dribbles_success}*"
