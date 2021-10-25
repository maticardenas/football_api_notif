from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from deep_translator import GoogleTranslator

from src.entities import Fixture, Team
from src.utils.date_utils import TimeZones, get_time_in_time_zone


def get_champions_league_fixtures(
    all_team_fixtures: Dict[str, Any]
) -> List[Dict[str, str]]:
    return [
        fixture
        for fixture in all_team_fixtures["response"]
        if fixture["league"]["id"] == 2
    ]


def date_diff(date: str) -> datetime:
    return datetime.strptime(date[:-6], "%Y-%m-%dT%H:%M:%S") - datetime.now()


def get_next_fixture(team_fixtures: List[Dict[str, Any]]) -> Optional[Fixture]:
    min_fixture = None
    min_diff = 999999999

    for fixture in team_fixtures:
        fixture_date_diff = int(date_diff(fixture["fixture"]["date"]).total_seconds())

        if not min_fixture and fixture_date_diff >= 0:
            min_fixture = fixture
            min_diff = fixture_date_diff

        if fixture_date_diff >= 0 and (fixture_date_diff < min_diff):
            min_fixture = fixture
            min_diff = fixture_date_diff

    return __convert_fixture_response(min_fixture, min_diff) if min_fixture else None


def __convert_fixture_response(
    fixture_response: Dict[str, Any], date_diff: int
) -> Fixture:
    utc_date = datetime.strptime(
        fixture_response["fixture"]["date"][:-6], "%Y-%m-%dT%H:%M:%S"
    )
    ams_date = get_time_in_time_zone(utc_date, TimeZones.AMSTERDAM)
    bsas_date = get_time_in_time_zone(utc_date, TimeZones.BSAS)

    league_name, round_name = __get_translated_league_name_and_round(fixture_response)

    return Fixture(
        utc_date,
        ams_date,
        bsas_date,
        date_diff,
        fixture_response["fixture"]["referee"],
        fixture_response["fixture"]["status"]["long"],
        league_name,
        round_name,
        Team(
            fixture_response["teams"]["home"]["name"],
            fixture_response["teams"]["home"]["logo"],
        ),
        Team(
            fixture_response["teams"]["away"]["name"],
            fixture_response["teams"]["away"]["logo"],
        ),
    )


def __get_translated_league_name_and_round(
    fixture_response: Dict[str, Any]
) -> Tuple[str, str]:
    if __is_team_or_league_for_spanish_translation(fixture_response):
        google_translator = GoogleTranslator(source="en", target="es")
        league_name = google_translator.translate(fixture_response["league"]["name"])
        round_name = google_translator.translate(fixture_response["league"]["round"])
    else:
        league_name = fixture_response["league"]["name"]
        round_name = fixture_response["league"]["round"]

    return (league_name, round_name)


def __is_team_or_league_for_spanish_translation(
    fixture_response: Dict[str, Any]
) -> bool:
    return fixture_response["league"][
        "country"
    ].lower() == "argentina" or __teams_contain(fixture_response, "argentina")


def __teams_contain(fixture_response: Dict[str, Any], text: str) -> bool:
    return any(
        [
            team_name
            for team_name in [
                fixture_response["teams"]["home"]["name"],
                fixture_response["teams"]["away"]["name"],
            ]
            if text in team_name.lower()
        ]
    )
