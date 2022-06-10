from datetime import datetime
from typing import Optional, List

from sqlmodel import Field, SQLModel, create_engine

class League(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    country: str
    logo: str


class Team(SQLModel, table=True):
    id: str = Field(primary_key=True)
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


sqlite_url = "postgresql://localhost:5432/notifier_db"

engine = create_engine(
    sqlite_url,
    connect_args={"user": "postgres", "password": "supersecretpassword"},
    echo=True)

SQLModel.metadata.create_all(engine)