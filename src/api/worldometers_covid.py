from typing import Any, Dict

from config.notif_config import NotifConfig
from src.request import APIRequest


class WorldometersClient:
    def __init__(self) -> None:
        super().__init__()
        self.base_url = f"https://{NotifConfig.X_WORLDOMETERS_HOST}"
        self.headers = {
            "x-rapidapi-host": NotifConfig.X_WORLDOMETERS_HOST,
            "x-rapidapi-key": NotifConfig.X_RAPIDAPI_KEY,
        }
        self.request = APIRequest()

    def get_stats_by_country(self, country: str) -> Dict[str, Any]:
        endpoint = "/api/coronavirus/country/"
        url = f"{self.base_url}{endpoint}{country}"

        return self.request.get(url, params={}, headers=self.headers)
