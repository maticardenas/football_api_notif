from typing import Any, Dict

from src.api.base_client import BaseClient
from src.request import APIRequest


class PlayersClient(BaseClient):
    def __init__(self) -> None:
        super().__init__()
        self.endpoint = "/v3/players"
        self.request = APIRequest()

    def get_players_stats_by(self, season: int, player_id: int) -> Dict[str, Any]:
        params = {"season": season, "id": player_id}
        url = f"{self.base_url}{self.endpoint}"

        return self.request.get(url, params, self.headers)
