from datetime import datetime, timedelta
from typing import List, Optional

from sqlmodel import select, or_

from src.db.db_manager import NotifierDBManager
from src.db.notif_sql_models import (
    Fixture as DBFixture,
    Team as DBTeam,
    League as DBLeague,
    Standing as DBStanding,
)
from src.entities import Championship, Team, FixtureForDB, TeamStanding
from src.notifier_logger import get_logger
from src.utils.date_utils import get_time_in_time_zone, TimeZones

logger = get_logger(__name__)


class FixturesDBManager:
    def __init__(self):
        self._notifier_db_manager = NotifierDBManager()

    def get_all_fixtures(self) -> List[Optional[DBFixture]]:
        return self._notifier_db_manager.select_records(select(DBFixture))

    def get_games_in_following_n_days(self, days: int) -> List[Optional[DBFixture]]:
        fixtures = []

        for day in range(1, days + 1):
            today = datetime.today()
            following_day = today + timedelta(days=day)
            bsas_date = get_time_in_time_zone(following_day, TimeZones.BSAS)
            tomorrow_str = bsas_date.strftime("%Y-%m-%d")

            statement = select(DBFixture).where(DBFixture.utc_date.contains(tomorrow_str))
            fixtures = fixtures + self._notifier_db_manager.select_records(statement)

        return fixtures

    def get_tomorrow_games(self) -> List[Optional[DBFixture]]:
        today = datetime.today()
        tomorrow = today + timedelta(days=1)
        bsas_date = get_time_in_time_zone(tomorrow, TimeZones.BSAS)
        tomorrow_str = bsas_date.strftime("%Y-%m-%d")

        statement = select(DBFixture).where(DBFixture.utc_date.contains(tomorrow_str))

        return self._notifier_db_manager.select_records(statement)

    def get_today_games(self) -> List[Optional[DBFixture]]:
        today = datetime.today()
        bsas_date = get_time_in_time_zone(today, TimeZones.BSAS)
        today_str = bsas_date.strftime("%Y-%m-%d")

        statement = select(DBFixture).where(DBFixture.utc_date.contains(today_str))

        return self._notifier_db_manager.select_records(statement)

    def get_yesterday_games(self) -> List[Optional[DBFixture]]:
        today = datetime.today()
        yesterday = today - timedelta(days=1)
        bsas_date = get_time_in_time_zone(yesterday, TimeZones.BSAS)
        yesterday_str = bsas_date.strftime("%Y-%m-%d")

        statement = select(DBFixture).where(DBFixture.utc_date.contains(yesterday_str))

        return self._notifier_db_manager.select_records(statement)

    def get_head_to_head_fixtures(self, team_1: str, team_2: str):
        statement = (
            select(DBFixture)
            .where(
                or_(DBFixture.home_team == team_1, DBFixture.away_team == team_1),
            )
            .where(or_(DBFixture.home_team == team_2, DBFixture.away_team == team_2))
            .order_by(DBFixture.utc_date)
        )

        fixtures = self._notifier_db_manager.select_records(statement)

        return [fixture for fixture in fixtures if fixture.home_score is not None]

    def insert_league(self, fixture_league: Championship) -> DBLeague:
        league_statement = select(DBLeague).where(
            DBLeague.id == fixture_league.league_id
        )
        retrieved_league = self._notifier_db_manager.select_records(league_statement)

        if not len(retrieved_league):
            logger.info(
                f"Inserting League {fixture_league.name} - it does not exist "
                f"in the database"
            )
            db_league = DBLeague(
                id=fixture_league.league_id,
                name=fixture_league.name,
                logo=fixture_league.logo,
                country=fixture_league.country,
            )
        else:
            logger.info(
                f"Updating League '{fixture_league.name}' - it already exists in "
                f"the database"
            )
            db_league = retrieved_league.pop()
            db_league.name = fixture_league.id
            db_league.logo = fixture_league.logo
            db_league.country = fixture_league.country

        self._notifier_db_manager.insert_record(db_league)

        return db_league

    def insert_team(self, fixture_team: Team) -> DBTeam:
        team_statement = select(DBTeam).where(DBTeam.id == fixture_team.id)
        retrieved_team = self._notifier_db_manager.select_records(team_statement)

        if not len(retrieved_team):
            logger.info(
                f"Inserting Team {fixture_team.name} - it does not exist in "
                f"the database"
            )
            db_team = DBTeam(
                id=fixture_team.id,
                name=fixture_team.name,
                picture=fixture_team.picture,
                aliases=fixture_team.aliases,
            )

        else:
            logger.info(
                f"Updating Team '{fixture_team.name}' - it already exists in "
                f"the database"
            )
            db_team = retrieved_team.pop()
            db_team.name = fixture_team.id
            db_team.picture = fixture_team.picture
            db_team.aliases = fixture_team.aliases

        self._notifier_db_manager.insert_record(db_team)

        return db_team

    def insert_team_standing(self, team_id: int, team_standing: TeamStanding) -> DBStanding:
        team_standing_statement = select(DBStanding).where(DBStanding.team == team_id, DBStanding.league == team_standing.championship.league_id)
        retrieved_team_standing = self._notifier_db_manager.select_records(
            team_standing_statement
        )

        if not len(team_standing_statement):
            logger.info(
                f"Inserting Team Standing - team {team_id} & {team_standing.championship.name} - it does not exist in "
                f"the database"
            )
            db_team_standing = DBStanding(
                league=team_standing.championship.league_id,
                team=team_id,
                position=team_standing.position,
                goal_diff=team_standing.goal_difference,
                current_condition=team_standing.current_condition
            )
        else:
            logger.info(
                f"Updating Team Standing team {team_id} & {team_standing.championship.name} - it already exists in "
                f"the database"
            )
            db_team_standing = retrieved_team_standing
            db_team_standing.league = team_standing.championship.league_id
            db_team_standing.team = team_id
            db_team_standing.position = team_standing.position
            db_team_standing.goal_diff = team_standing.goal_difference
            db_team_standing.current_condition = team_standing.current_condition

        self._notifier_db_manager.insert_record(db_team_standing)

        return db_team_standing

    def save_fixtures(self, team_fixtures: List[FixtureForDB]) -> None:
        db_fixtures = []

        for conv_fix in team_fixtures:
            retrieved_league = self.insert_league(conv_fix.championship)
            retrieved_home_team = self.insert_team(conv_fix.home_team)
            retrieved_away_team = self.insert_team(conv_fix.away_team)

            fixture_statement = select(DBFixture).where(DBFixture.id == conv_fix.id)
            retrieved_fixture = self._notifier_db_manager.select_records(
                fixture_statement
            )

            if not len(retrieved_fixture):
                logger.info(
                    f"Inserting Fixture {conv_fix.home_team.name} vs "
                    f"{conv_fix.away_team.name} - it does not exist in the "
                    f"database"
                )
                db_fixture = DBFixture(
                    id=conv_fix.id,
                    utc_date=conv_fix.utc_date,
                    league=retrieved_league.pop().id,
                    round=conv_fix.round,
                    home_team=retrieved_home_team.id,
                    away_team=retrieved_away_team.id,
                    home_score=conv_fix.match_score.home_score,
                    away_score=conv_fix.match_score.away_score,
                )
            else:
                logger.info(
                    f"Updating Fixture {conv_fix.home_team.name} vs "
                    f"{conv_fix.away_team.name}"
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

        self._notifier_db_manager.insert_records(db_fixtures)
