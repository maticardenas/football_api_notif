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


class ManagedTeam(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    team_command: str
    team_id: int = Field(foreign_key="team.id")


class NotifSubscription(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    chat_id: str
    team_ids: List[int] = Field(foreign_key="team.id")


class Fixture(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: int = Field(primary_key=True)
    utc_date: str
    league: int = Field(foreign_key="league.id")
    round: str
    home_team: int = Field(foreign_key="team.id")
    away_team: int = Field(foreign_key="team.id")
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    highlights: Optional[List[str]]
