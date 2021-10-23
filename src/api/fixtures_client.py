from typing import Any, Dict

from src.api.base_client import BaseClient
from src.request import APIRequest


class FixturesClient(BaseClient):
    def __init__(self) -> None:
        super().__init__()
        self.endpoint = "/v3/fixtures"
        self.request = APIRequest()

    def get_fixtures_by(self, season: int, team_id: int) -> Dict[str, Any]:
        params = {"season": season, "team": team_id}
        url = f"{self.base_url}{self.endpoint}"

        return self.request.get(url, params, self.headers)
