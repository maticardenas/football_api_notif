import random
from typing import List, Tuple

from sqlmodel import or_, select

from config.config_entities import ManagedTeam
from config.config_utils import get_managed_teams_config
from src.db.db_manager import NotifierDBManager
from src.db.notif_sql_models import Fixture
from src.emojis import Emojis
from src.telegram_bot.bot_constants import MESSI_PHOTO
from src.utils.fixtures_utils import (
    get_today_fixture_db,
    get_yesterday_fixture_db,
    get_tomorrow_fixture_db,
)


class NotifierBotCommandsHandler:
    def __init__(self):
        self._managed_teams = get_managed_teams_config()
        self._notifier_db_manager = NotifierDBManager()

    def get_managed_team(self, command_name: str) -> ManagedTeam:
        return next(
            (team for team in self._managed_teams if team.command_name == command_name),
            None,
        )

    def is_available_team(self, team: str) -> bool:
        return any(
            managed_team
            for managed_team in self._managed_teams
            if managed_team.command_name == team
        )

    def available_command_team_names(self) -> List[str]:
        return [managed_team.command_name for managed_team in self._managed_teams]

    def available_teams_text(self) -> str:
        return "\n".join(
            [
                f"• {available_team}"
                for available_team in self.available_command_team_names()
            ]
        )

    def _get_all_fixtures_ids(self, fixtures: List[Fixture]) -> List[str]:
        return [fixture.id for fixture in fixtures]

    def _get_date_games_fixtures(self, criteria: str = "today") -> List[str]:
        """
        This method retrieves the fixtures for all managed teams according to certain "criteria"

        :param criteria: date to get fixtures from
        :return: fixtures according to the criteria
        """
        games = []

        retrieve_date_methods = {
            "today": get_today_fixture_db,
            "yesterday": get_yesterday_fixture_db,
            "tomorrow": get_tomorrow_fixture_db,
        }

        retrieve_method = retrieve_date_methods.get(criteria, get_today_fixture_db)

        for team in self._managed_teams:
            statement = select(Fixture).where(
                or_(
                    Fixture.home_team == team.id,
                    Fixture.away_team == team.id,
                )
            )
            team_fixtures = self._notifier_db_manager.select_records(statement)

            fixture = retrieve_method(team_fixtures)

            if fixture:
                if fixture.id not in self._get_all_fixtures_ids(games):
                    games.append(retrieve_method(team_fixtures))

        return games

    def today_games(self, user_name: str) -> Tuple[str, str]:
        today_games_fixtures = self._get_date_games_fixtures("today")

        if len(today_games_fixtures):
            today_games_text = "\n\n".join(
                [fixture.one_line_telegram_repr() for fixture in today_games_fixtures]
            )
            today_games_text_intro = (
                f"{Emojis.WAVING_HAND.value} Hola "
                f"{user_name}, "
                f"estos son los partidos de hoy:\n\n"
            )
            text = f"{today_games_text_intro}{today_games_text}"
            leagues = [fixture.championship for fixture in today_games_fixtures]
            photo = random.choice([league.logo for league in leagues])
        else:
            text = (
                f"{Emojis.WAVING_HAND.value} Hola "
                f"{user_name}, lamentablemente hoy "
                f"no hay partidos :("
            )
            photo = MESSI_PHOTO

        return (text, photo)

    def yesterday_games(self, user_name: str) -> Tuple[str, str]:
        played_games_fixtures = self._get_date_games_fixtures("yesterday")

        if len(played_games_fixtures):
            played_games_text = "\n\n".join(
                [
                    fixture.one_line_telegram_repr(played=True)
                    for fixture in played_games_fixtures
                ]
            )
            played_games_text_intro = (
                f"{Emojis.WAVING_HAND.value} Hola "
                f"{user_name}, "
                f"estos son los partidos jugados "
                f"ayer:\n\n"
            )
            text = f"{played_games_text_intro}{played_games_text}"
            leagues = [fixture.championship for fixture in played_games_fixtures]
            photo = random.choice([league.logo for league in leagues])
        else:
            text = (
                f"{Emojis.WAVING_HAND.value} Hola "
                f"{user_name}, lamentablemente "
                f"ayer no se jugaron partidos :("
            )
            photo = MESSI_PHOTO

        return (text, photo)

    def tomorrow_games(self, user_name: str) -> Tuple[str, str]:
        tomorrow_games_fixtures = self._get_date_games_fixtures("tomorrow")

        if len(tomorrow_games_fixtures):
            tomorrow_games_text = "\n\n".join(
                [
                    fixture.one_line_telegram_repr()
                    for fixture in tomorrow_games_fixtures
                ]
            )
            tomorrow_games_text_intro = (
                f"{Emojis.WAVING_HAND.value} Hola "
                f"{user_name}, "
                f"estos son los partidos de mañana:\n\n"
            )
            text = f"{tomorrow_games_text_intro}{tomorrow_games_text}"
            leagues = [fixture.championship for fixture in tomorrow_games_fixtures]
            photo = random.choice([league.logo for league in leagues])
        else:
            text = (
                f"{Emojis.WAVING_HAND.value} Hola "
                f"{user_name}, lamentablemente mañana "
                f"no hay partidos :("
            )
            photo = MESSI_PHOTO

        return (text, photo)


class NextAndLastMatchCommandHandler(NotifierBotCommandsHandler):
    def __init__(self, commands_args: List[str]):
        super().__init__()
        self._command_args = commands_args

    def validate_command_input(self) -> str:
        response = ""

        if len(self._command_args) < 1:
            response = "Debés ingresar al menos un equipo"
        elif len(self._command_args) > 1:
            response = "Sólo puedes ingresar un equipo"
        else:
            team = self._command_args[0].lower()
            if not self.is_available_team(team):
                response = (
                    f"Oops! '{team}' no está disponible :(\n\n"
                    f"Los equipos disponibles son:\n\n"
                    f"{self.available_teams_text()}"
                )

        return response
