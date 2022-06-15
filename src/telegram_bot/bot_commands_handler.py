from typing import List

from config.config_entities import ManagedTeam
from config.config_utils import get_managed_teams_config


class NotifierBotCommandsHandler:
    def __init__(self):
        self._managed_teams = get_managed_teams_config()

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
