import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from unittest.mock import patch, MagicMock

from freezegun import freeze_time

from src.fixtures_utils import get_next_fixture
from src.players_utils import convert_player_stats, get_str_stats_summary
from tests.utils.sample_data_utils import get_sample_data_response

DATA_PATH = Path.cwd().joinpath('data')


def test_convert_player_stats():
    # given
    player_response_json_file = "player_statistics_sample.json"
    player_response = get_sample_data_response(DATA_PATH, player_response_json_file)

    # when
    players_stats = convert_player_stats(player_response[0])

    # then
    assert "Paris Saint Germain" in players_stats
    assert "Ligue 1" in players_stats["Paris Saint Germain"]
    assert "UEFA Champions League" in players_stats["Paris Saint Germain"]
    assert "Club Friendlies" in players_stats["Paris Saint Germain"]
    assert "Barcelona" in players_stats
    assert "Club Friendlies" in players_stats["Barcelona"]
    assert "Argentina" in players_stats
    assert "Copa America" in players_stats["Argentina"]
