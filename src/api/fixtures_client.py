from typing import Any, Dict

from src.api.base_client import BaseClient
from src.request import APIRequest


class FixturesClient(BaseClient):
    def __init__(self) -> None:
        super().__init__()
        self.request = APIRequest()

    def get_fixtures_by(self, season: int, team_id: int) -> Dict[str, Any]:
        endpoint = "/v3/fixtures"
        params = {"season": season, "team": team_id}
        url = f"{self.base_url}{endpoint}"

        return self.request.get(url, params, self.headers)

    def get_standings_by(self, season: int, team_id: int) -> Dict[str, Any]:
        endpoint = "/v3/standings"
        params = {"season": season, "team": team_id}
        url = f"{self.base_url}{endpoint}"

        return self.request.get(url, params, self.headers)

    def get_team_information(self, team_id: int) -> Dict[str, Any]:
        endpoint = "/v3/teams"
        params = {"id": team_id}
        url = f"{self.base_url}{endpoint}"

        return self.request.get(url, params, self.headers)

    def get_line_up(self, fixture_id: int, team_id: int) -> Dict[str, Any]:
        endpoint = "/v3/fixtures/lineups"
        params = {"fixture": fixture_id, "team": team_id}
        url = f"{self.base_url}{endpoint}"

        return self.request.get(url, params, self.headers)
