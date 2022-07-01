from datetime import date
from typing import List

from config.config_utils import get_managed_teams_config
from src.api.fixtures_client import FixturesClient
from src.db.fixtures_db_manager import FixturesDBManager
from src.notifier_logger import get_logger
from src.team_fixtures_manager import TeamFixturesManager
from src.utils.fixtures_utils import convert_fixture_response_to_db

FIXTURES_DB_MANAGER = FixturesDBManager()
MANAGED_TEAMS = get_managed_teams_config()

logger = get_logger(__name__)


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
        logger.info(f"Updating fixtures for lot {lot}")
        team_fixtures = fixtures_client.get_fixtures_by(ids=lot)
        FIXTURES_DB_MANAGER.save_fixtures(
            [convert_fixture_response_to_db(fixture) for fixture in team_fixtures.as_dict["response"]]
        )


def get_fixture_update_lots(
    fixtures_to_update: List[int], lot_size: int = 20
) -> List[List[int]]:
    for i in range(0, len(fixtures_to_update), lot_size):
        yield fixtures_to_update[i : i + lot_size]


def get_all_fixtures_to_update() -> List["DBFixture"]:
    all_fixtures_to_update = []
    for team in MANAGED_TEAMS:
        logger.info(f"Getting surrounding fixtures for team {team.name}")
        team_fixtures_manager = TeamFixturesManager(date.today().year, team.id)
        all_fixtures_to_update.append(team_fixtures_manager.get_next_team_fixture())
        all_fixtures_to_update.append(team_fixtures_manager.get_last_team_fixture())

    return [fixture.id for fixture in all_fixtures_to_update if fixture]


if __name__ == "__main__":
    update_fixtures()
