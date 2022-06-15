from datetime import date
from typing import List

from sqlmodel import select

from config.config_utils import get_managed_teams_config
from src.api.fixtures_client import FixturesClient
from src.db.db_manager import NotifierDBManager
from src.db.notif_sql_models import Fixture as DBFixture
from src.db.notif_sql_models import League as DBLeague
from src.db.notif_sql_models import Team as DBTeam
from src.entities import Championship, Team
from src.utils.fixtures_utils import convert_fixture_response_to_db

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
    fix_nr = 1
    for fixture in team_fixtures:
        print(f"Converting & populating fixture {fix_nr}/{len(team_fixtures)}")
        converted_fixtures.append(convert_fixture_response_to_db(fixture))
        fix_nr += 1

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
                league=retrieved_league.pop().id,
                round=conv_fix.round,
                home_team=retrieved_home_team.pop().id,
                away_team=retrieved_away_team.pop().id,
                home_score=conv_fix.match_score.home_score,
                away_score=conv_fix.match_score.away_score,
            )
        else:
            db_fixture = retrieved_fixture.pop()
            db_fixture.id = conv_fix.id
            db_fixture.utc_date = conv_fix.utc_date
            db_fixture.league = retrieved_league.pop().id
            db_fixture.round = conv_fix.round
            db_fixture.home_team = retrieved_home_team.pop().id
            db_fixture.away_team = retrieved_away_team.pop().id
            db_fixture.home_score = conv_fix.match_score.home_score
            db_fixture.away_score = conv_fix.match_score.away_score

        db_fixtures.append(db_fixture)

    NOTIFIER_DB_MANAGER.insert_records(db_fixtures)


def populate_data(is_initial: bool = False) -> None:
    managed_teams = get_managed_teams_config()
    fixtures_client = FixturesClient()
    current_year = date.today().year
    last_year = current_year - 1

    for team in managed_teams:
        if is_initial:
            team_fixtures = fixtures_client.get_fixtures_by(str(last_year), team.id)
            if "response" in team_fixtures.as_dict:
                save_fixtures(team_fixtures.as_dict["response"])

        team_fixtures = fixtures_client.get_fixtures_by(str(current_year), team.id)
        if "response" in team_fixtures.as_dict:
            save_fixtures(team_fixtures.as_dict["response"])


if __name__ == "__main__":
    fixtures = NOTIFIER_DB_MANAGER.select_records(select(DBFixture))
    is_initial = True if not len(fixtures) else False
    populate_data(is_initial)
