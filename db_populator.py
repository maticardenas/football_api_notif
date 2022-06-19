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
from src.notifier_logger import get_logger
from src.team_fixtures_manager import TeamFixturesManager
from src.utils.fixtures_utils import convert_fixture_response_to_db

NOTIFIER_DB_MANAGER = NotifierDBManager()

MANAGED_TEAMS = get_managed_teams_config()

logger = get_logger(__name__)


def insert_league(fixture_league: Championship) -> DBLeague:
    league_statement = select(DBLeague).where(DBLeague.id == fixture_league.league_id)
    retrieved_league = NOTIFIER_DB_MANAGER.select_records(league_statement)

    if not len(retrieved_league):
        logger.info(
            f"Inserting League {fixture_league.name} - it does not exist in the database"
        )
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
        logger.info(
            f"Inserting Team {fixture_team.name} - it does not exist in the database"
        )
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
        fixture_match = (
            f'{fixture["teams"]["home"]["name"]} vs. {fixture["teams"]["away"]["name"]}'
        )
        logger.info(
            f"Converting & populating fixture {fix_nr}/{len(team_fixtures)} - {fixture_match}"
        )
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
            logger.info(
                f"Inserting Fixture {conv_fix.home_team.name} vs {conv_fix.away_team.name} - it does not exist in the database"
            )
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
            logger.info(
                f"Updating Fixture {conv_fix.home_team.name} vs {conv_fix.away_team.name}"
            )
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


def populate_initial_data() -> None:
    fixtures_client = FixturesClient()
    current_year = date.today().year
    last_year = current_year - 1

    for team in MANAGED_TEAMS:
        logger.info(f"Saving fixtures for team {team.name}")
        team_fixtures = fixtures_client.get_fixtures_by(str(last_year), team.id)
        if "response" in team_fixtures.as_dict:
            save_fixtures(team_fixtures.as_dict["response"])

        team_fixtures = fixtures_client.get_fixtures_by(str(current_year), team.id)
        if "response" in team_fixtures.as_dict:
            save_fixtures(team_fixtures.as_dict["response"])


def update_fixtures() -> None:
    """
    This function updates only fixtures corresponding to the
    last & next match for each managed team, given that this is
    at the moment the only that the user can query, doesn't make sense to
    query all the fixtures for all teams. This way we can save dozens of
    RAPID API hits per day, giving space to multiple other functionalities.
    """
    fixtures_client = FixturesClient()
    fixtures_to_update = get_all_fixtures_to_update()
    lots_to_update = get_fixture_update_lots(fixtures_to_update)

    for lot in lots_to_update:
        team_fixtures = fixtures_client.get_fixtures_by(ids=lot)
        save_fixtures(team_fixtures.as_dict["response"])


def get_fixture_update_lots(
    fixtures_to_update: List[int], lot_size: int = 20
) -> List[List[int]]:
    for i in range(0, len(fixtures_to_update), lot_size):
        yield fixtures_to_update[i : i + lot_size]


def get_all_fixtures_to_update() -> List[DBFixture]:
    all_fixtures_to_update = []
    for team in MANAGED_TEAMS:
        team_fixtures_manager = TeamFixturesManager(date.today().year, team.id)
        all_fixtures_to_update.append(team_fixtures_manager.get_next_team_fixture())
        all_fixtures_to_update.append(team_fixtures_manager.get_last_team_fixture())

    return [fixture.id for fixture in all_fixtures_to_update if fixture]


if __name__ == "__main__":
    logger.info("Populating data...")
    fixtures = NOTIFIER_DB_MANAGER.select_records(select(DBFixture))
    is_initial = True if not len(fixtures) else False

    logger.info(f"IS_INITIAL -> {is_initial}")

    if is_initial:
        populate_initial_data()
    else:
        update_fixtures()
