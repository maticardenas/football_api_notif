from typing import Any, Dict

from config.rapidapi import X_RAPIDAPI_KEY, X_WORLDOMETERS_HOST
from src.request import APIRequest


class WorldometersClient:
    def __init__(self) -> None:
        super().__init__()
        self.base_url = f"https://{X_WORLDOMETERS_HOST}"
        self.headers = {
            "x-rapidapi-host": X_WORLDOMETERS_HOST,
            "x-rapidapi-key": X_RAPIDAPI_KEY,
        }
        self.request = APIRequest()

    def get_stats_by_country(self, country: str) -> Dict[str, Any]:
        endpoint = "/api/coronavirus/country/"
        url = f"{self.base_url}{endpoint}{country}"

        return self.request.get(url, params={}, headers=self.headers)
