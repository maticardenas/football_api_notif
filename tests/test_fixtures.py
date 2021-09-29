import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from unittest.mock import patch, MagicMock

from freezegun import freeze_time

from src.fixtures_utils import get_next_fixture

DATA_PATH = Path.cwd().joinpath('data')


def test_get_next_fixture():
    # given
    fixture_response = get_test_fixture_response()

    # when
    with freeze_time("2021-09-29 18:30:00"):
        next_fixture = get_next_fixture(fixture_response)

    # then
    assert next_fixture.date == '2021-09-29T18:45:00+00:00'
    assert next_fixture.home_team == 'Peterborough'
    assert next_fixture.away_team == 'Bournemouth'
    assert next_fixture.championship == 'Championship'
    assert next_fixture.match_status == 'Not Started'
    assert next_fixture.referee == 'A.  Woolmer'
    assert next_fixture.round == 'Regular Season - 10'


def get_test_fixture_response() -> Dict[str, Any]:
    path = DATA_PATH.joinpath("fixtures_response_sample.json")

    with path.open(mode='r') as f:
        return json.load(f)["response"]
