from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, SQLModel


class League(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: int = Field(primary_key=True)
    name: str
    country: str
    logo: str


class Team(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: int = Field(primary_key=True)
    name: str
    picture: str
    aliases: Optional[List[str]]


class Fixture(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: int = Field(primary_key=True)
    utc_date: str
    league: int = Field(foreign_key="league.id")
    round: str
    home_team: int = Field(foreign_key="team.id")
    away_team: int = Field(foreign_key="team.id")
    line_up: Optional[int] = Field(foreign_key="lineup.id")
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    highlights: Optional[List[str]]


class Player(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: int = Field(primary_key=True)
    name: str
    pos: str
    picture: str


class LineUp(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: int = Field(primary_key=True)
    formation: str
    goalkeeper: int = Field(foreign_key="player.id")
    defenders: List[int] = Field(foreign_key="player.id")
    midfielders: List[int] = Field(foreign_key="player.id")
    forward_strikers: List[int] = Field(foreign_key="player.id")
