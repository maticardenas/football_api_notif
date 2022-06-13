from unittest.mock import patch

import pytest

from config.config_entities import ManagedTeam
from src.telegram_bot.bot_commands_handler import NotifierBotCommandsHandler


@patch("src.telegram_bot.bot_commands_handler.get_managed_teams_config")
def test_get_managed_team(mocked_get_managed_teams_config):
    # given
    managed_team_river = ManagedTeam(
            "435",
            "River Plate",
            "river",
        )
    managed_team_psg = ManagedTeam(
            "85",
            "Paris Saint Germain",
            "psg",
        )
    mocked_get_managed_teams_config.return_value = [managed_team_river, managed_team_psg]
    notifier_commands_handler = NotifierBotCommandsHandler()

    # when
    managed_team = notifier_commands_handler.get_managed_team("psg")

    # then
    assert managed_team == managed_team_psg


@patch("src.telegram_bot.bot_commands_handler.get_managed_teams_config")
def test_available_command_team_names(mocked_get_managed_teams_config):
    # given
    managed_team_river = ManagedTeam(
        "435",
        "River Plate",
        "river",
    )
    managed_team_psg = ManagedTeam(
        "85",
        "Paris Saint Germain",
        "psg",
    )
    mocked_get_managed_teams_config.return_value = [managed_team_river, managed_team_psg]
    notifier_commands_handler = NotifierBotCommandsHandler()

    # when
    available_command_team_names = notifier_commands_handler.available_command_team_names()

    # then
    assert available_command_team_names == ["river", "psg"]



@pytest.mark.parametrize(
    "team, is_available",
    [
        ("river", True),
        ("psg", True),
        ("mancity", False)
    ]
)
@patch("src.telegram_bot.bot_commands_handler.get_managed_teams_config")
def test_is_available_team(mocked_get_managed_teams_config, team: str, is_available: bool):
    # given
    managed_team_river = ManagedTeam(
        "435",
        "River Plate",
        "river",
    )
    managed_team_psg = ManagedTeam(
        "85",
        "Paris Saint Germain",
        "psg",
    )
    mocked_get_managed_teams_config.return_value = [managed_team_river, managed_team_psg]
    notifier_commands_handler = NotifierBotCommandsHandler()

    # when - then
    assert notifier_commands_handler.is_available_team(team) == is_available