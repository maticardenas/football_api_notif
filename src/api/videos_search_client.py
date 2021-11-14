from typing import Any, Dict

from config.rapidapi import (X_RAPIDAPI_IMG_SEARCH_HOST, X_RAPIDAPI_KEY,
                             X_RAPIDAPI_VIDEO_SEARCH_HOST)
from src.api.base_client import BaseClient
from src.request import APIRequest


class VideosSearchClient:
    def __init__(self) -> None:
        super().__init__()
        self.base_url = f"https://{X_RAPIDAPI_VIDEO_SEARCH_HOST}"
        self.headers = {
            "x-rapidapi-host": X_RAPIDAPI_VIDEO_SEARCH_HOST,
            "x-rapidapi-key": X_RAPIDAPI_KEY,
        }
        self.request = APIRequest()

    def search_football_videos(self) -> Dict[str, Any]:
        return self.request.get(self.base_url, {}, self.headers)
