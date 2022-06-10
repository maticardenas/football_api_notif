from datetime import datetime
from typing import Optional, List

from sqlmodel import Field, SQLModel


class League(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    country: str
    logo: str


class Team(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    picture: str
    aliases: Optional[List[str]]


class Fixture(SQLModel, table=True):
    id: int = Field(primary_key=True)
    utc_date: datetime
    bsas_date: datetime
    ams_date: datetime
    utc_date: datetime
    league: League = Field(foreign_key="league.id")
    round: str
    home_team: Team = Field(foreign_key="team.id")
    away_team: Team = Field(foreign_key="team.id")
    home_score: int
    away_score: int
    highlights: Optional[List[str]]
