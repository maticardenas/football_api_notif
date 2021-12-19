import re
import urllib
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import HTTPError

from deep_translator import GoogleTranslator

from src.api.fixtures_client import FixturesClient
from src.api.images_search_client import ImagesSearchClient
from src.api.videos_search_client import VideosSearchClient
from src.api.youtube_search_client import YoutubeSearchClient
from src.entities import (Championship, Fixture, LineUp, MatchHighlights,
                          MatchScore, Player, Team, TeamStanding)
from src.utils.date_utils import TimeZones, get_time_in_time_zone
from src.utils.message_utils import TEAMS_ALIASES


def get_team_aliases(team_id: str) -> list:
    return TEAMS_ALIASES.get(team_id, [])


def get_champions_league_fixtures(
    all_team_fixtures: Dict[str, Any]
) -> List[Dict[str, str]]:
    return [
        fixture
        for fixture in all_team_fixtures["response"]
        if fixture["league"]["id"] == 2
    ]


def date_diff(date: str) -> datetime:
    return datetime.strptime(date[:-6], "%Y-%m-%dT%H:%M:%S") - datetime.utcnow()


def get_next_fixture(
    team_fixtures: List[Dict[str, Any]], team_id: str
) -> Optional[Fixture]:
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

    return (
        __convert_fixture_response(min_fixture, min_diff, team_id)
        if min_fixture
        else None
    )


def get_last_fixture(
    team_fixtures: List[Dict[str, Any]], team_id: str
) -> Optional[Fixture]:
    min_fixture = None
    min_diff = -999999999

    for fixture in team_fixtures:
        fixture_date_diff = int(date_diff(fixture["fixture"]["date"]).total_seconds())

        if not min_fixture and fixture_date_diff < 0:
            min_fixture = fixture
            min_diff = fixture_date_diff

        if fixture_date_diff < 0 and (fixture_date_diff > min_diff):
            min_fixture = fixture
            min_diff = fixture_date_diff

    return (
        __convert_fixture_response(min_fixture, min_diff, team_id)
        if min_fixture
        else None
    )


def get_team_standings_for_league(team_standings: dict, league_id: int) -> TeamStanding:
    for team_standing in team_standings:
        if team_standing["league"]["id"] == league_id:
            return __convert_standing_response(team_standing)


def __convert_standing_response(team_standing: dict) -> TeamStanding:
    standing_desc = team_standing["league"]["standings"][0][0]
    return TeamStanding(
        Championship(
            team_standing["league"]["id"],
            team_standing["league"]["name"],
            team_standing["league"]["country"],
            team_standing["league"]["logo"],
        ),
        standing_desc["rank"],
        standing_desc["points"],
        standing_desc["goalsDiff"],
        standing_desc["description"],
    )


def __convert_fixture_response(
    fixture_response: Dict[str, Any], date_diff: int, team_id: str
) -> Fixture:
    utc_date = datetime.strptime(
        fixture_response["fixture"]["date"][:-6], "%Y-%m-%dT%H:%M:%S"
    )
    ams_date = get_time_in_time_zone(utc_date, TimeZones.AMSTERDAM)
    bsas_date = get_time_in_time_zone(utc_date, TimeZones.BSAS)

    league_name, round_name = __get_translated_league_name_and_round(fixture_response)
    home_team_id = fixture_response["teams"]["home"]["id"]
    away_team_id = fixture_response["teams"]["away"]["id"]

    return Fixture(
        utc_date,
        ams_date,
        bsas_date,
        date_diff,
        fixture_response["fixture"]["referee"],
        fixture_response["fixture"]["status"]["long"],
        Championship(
            fixture_response["league"]["id"],
            league_name,
            fixture_response["league"]["country"],
            fixture_response["league"]["logo"],
        ),
        round_name,
        Team(
            home_team_id,
            fixture_response["teams"]["home"]["name"],
            fixture_response["teams"]["home"]["logo"],
            get_team_aliases(str(home_team_id)),
        ),
        Team(
            away_team_id,
            fixture_response["teams"]["away"]["name"],
            fixture_response["teams"]["away"]["logo"],
            get_team_aliases(str(away_team_id)),
        ),
        MatchScore(
            fixture_response["goals"]["home"], fixture_response["goals"]["away"]
        ),
        get_line_up(fixture_response["fixture"]["id"], team_id),
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


def get_image_search(query: str) -> str:
    image_searcher = ImagesSearchClient()
    images = image_searcher.get_images(query)

    json_response = images.as_dict

    for image in json_response["value"]:
        url = image["contentUrl"]
        if is_url_reachable(url):
            return url

    return ""


def is_url_reachable(url: str) -> bool:
    try:
        response_code = urllib.request.urlopen(url).getcode()
    except HTTPError:
        print(f"The image url {url} is NOT reachable.")
        return False

    return response_code == 200


def get_match_highlights(fixture: Fixture) -> List[MatchHighlights]:
    videos_search_client = VideosSearchClient()
    latest_videos = videos_search_client.search_football_videos()

    match_highlights = []

    for match in latest_videos.as_dict:
        if is_corresponding_match_highlights(
            fixture.home_team, fixture.away_team, match["title"]
        ):
            if -3 <= date_diff(match["date"]).days <= 0:
                match_highlights = search_highlights_videos(match)
                break

    return [convert_match_highlights(highlights) for highlights in match_highlights]


def is_corresponding_match_highlights(
    home_team: Team, away_team: Team, match_title: str
) -> bool:
    return (
        home_team.name.lower() in match_title.lower()
        or away_team.name.lower() in match_title.lower()
        or any(
            [
                team_alias.lower() == match_title.lower()
                for team_alias in home_team.aliases + away_team.aliases
            ]
        )
    )


def convert_match_highlights(highlights: dict) -> MatchHighlights:
    url_match = re.search("http.*?'", highlights["embed"])
    highlights_url = highlights["embed"][url_match.span()[0] : url_match.span()[1] - 1]
    return MatchHighlights(highlights_url, highlights["embed"])


def search_highlights_videos(match_response):
    return [
        video for video in match_response["videos"] if video["title"] == "Highlights"
    ]


def get_youtube_highlights_videos(
    home_team: Team, away_team: Team, number_of_options=3
) -> List[str]:
    youtube_client = YoutubeSearchClient()
    response = youtube_client.search_videos_by_keywords(
        [home_team.name, away_team.name, "resumen", "jugadas"], "es", "ar"
    )

    json_response = response.as_dict

    video_highlights = []

    options_selected = 0

    try:
        for item in json_response["items"]:
            title = item["snippet"]["title"]
            home_team_words = home_team.name.lower().split(" ")
            away_team_words = away_team.name.lower().split(" ")
            if (
                any(ht_word in title.lower() for ht_word in home_team_words)
                or any(alias.lower() in title.lower() for alias in home_team.aliases)
            ) and (
                any(at_word in title.lower() for at_word in away_team_words)
                or any(alias.lower() in title.lower() for alias in away_team.aliases)
            ):
                video_highlights.append(item["url"])
                options_selected += 1

            if options_selected >= number_of_options:
                break
    except:
        print("There was an issue retrieving video highlights")

    return video_highlights


def get_line_up(fixture_id: str, team_id: str) -> Optional[LineUp]:
    fixture_client = FixturesClient()

    response = fixture_client.get_line_up(fixture_id, team_id)
    json_response = response.as_dict["response"]

    line_up = None

    if json_response:
        if "startXI" in json_response[0]:
            start_xi = json_response[0]["startXI"]
            line_up = LineUp(
                formation=json_response[0]["formation"],
                goalkeeper=get_players(start_xi, "G")[0],
                defenders=get_players(start_xi, "D"),
                midfielders=get_players(start_xi, "M"),
                forward_strikers=get_players(start_xi, "F"),
            )

    return line_up


def get_players(start_xi: dict, position: str) -> List[Player]:
    return [
        Player(
            player["player"]["id"], player["player"]["name"], player["player"]["pos"]
        )
        for player in start_xi
        if player["player"]["pos"] == position
    ]
