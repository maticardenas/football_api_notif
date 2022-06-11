import sys
from typing import List

from sqlmodel import select

from api.fixtures_client import FixturesClient
from db.db_manager import NotifierDBManager
from entities import Championship, Team

from src.db.notif_sql_models import (
    Fixture as DBFixture,
    League as DBLeague,
    Team as DBTeam,
)
from utils.fixtures_utils import date_diff, convert_fixture_response

NOTIFIER_DB_MANAGER = NotifierDBManager()


def insert_league(fixture_league: Championship) -> DBLeague:
    league_statement = select(DBLeague).where(DBLeague.id == fixture_league.league_id)
    retrieved_league = NOTIFIER_DB_MANAGER.select_records(league_statement)

    if not len(retrieved_league):
        league = DBLeague(
            id=fixture_league.league_id,
            name=fixture_league.name,
            logo=fixture_league.logo,
            country=fixture_league.country,
        )
        NOTIFIER_DB_MANAGER.insert_record(league)
        retrieved_league = NOTIFIER_DB_MANAGER.select_records(league_statement)

    return retrieved_league


def insert_team(fixture_team: Team) -> DBTeam:
    team_statement = select(DBTeam).where(DBTeam.id == fixture_team.id)
    retrieved_team = NOTIFIER_DB_MANAGER.select_records(team_statement)

    if not len(retrieved_team):
        team = DBTeam(
            id=fixture_team.id,
            name=fixture_team.name,
            picture=fixture_team.picture,
            aliases=fixture_team.aliases,
        )
        NOTIFIER_DB_MANAGER.insert_record(team)
        retrieved_team = NOTIFIER_DB_MANAGER.select_records(team_statement)

    return retrieved_team


def save_fixtures(team_fixtures: List[dict]) -> None:
    converted_fixtures = []
    for fixture in team_fixtures[:1]:
        fixture_date_diff = int(date_diff(fixture["fixture"]["date"]).total_seconds())
        converted_fixtures.append(convert_fixture_response(fixture, fixture_date_diff))

    db_fixtures = []
    for conv_fix in converted_fixtures:
        retrieved_league = insert_league(conv_fix.championship)
        retrieved_home_team = insert_team(conv_fix.home_team)
        retrieved_away_team = insert_team(conv_fix.away_team)

        fixture_statement = select(DBFixture).where(DBFixture.id == conv_fix.id)
        retrieved_fixture = NOTIFIER_DB_MANAGER.select_records(fixture_statement)

        if not len(retrieved_fixture):
            db_fixture = DBFixture(
                id=conv_fix.id,
                utc_date=conv_fix.utc_date,
                bsas_date=conv_fix.bsas_date,
                ams_date=conv_fix.ams_date,
                league=retrieved_league.pop().id,
                round=conv_fix.round,
                home_team=retrieved_home_team.pop().id,
                away_team=retrieved_away_team.pop().id,
                home_score=conv_fix.match_score.home_score,
                away_score=conv_fix.match_score.away_score,
            )
            db_fixtures.append(db_fixture)

    NOTIFIER_DB_MANAGER.insert_records(db_fixtures)


if __name__ == "__main__":
    season = sys.argv[1]
    team = sys.argv[2]
    fixtures_client = FixturesClient()
    team_fixtures = fixtures_client.get_fixtures_by(season, team)
    save_fixtures(team_fixtures.as_dict["response"])
