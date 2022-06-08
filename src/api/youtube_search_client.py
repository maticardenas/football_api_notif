from typing import Any, Dict, List

from config.rapidapi import (X_RAPIDAPI_IMG_SEARCH_HOST, X_RAPIDAPI_KEY,
                             X_RAPIDAPI_VIDEO_SEARCH_HOST,
                             X_YOUTUBE_SEARCH_HOST)
from src.api.base_client import BaseClient
from src.request import APIRequest


class YoutubeSearchClient:
    def __init__(self) -> None:
        super().__init__()
        self.base_url = f"https://{X_YOUTUBE_SEARCH_HOST}/get_keywords_video/v1"
        self.headers = {
            "content-type": "application/x-www-form-urlencoded",
            "x-rapidapi-host": X_YOUTUBE_SEARCH_HOST,
            "x-rapidapi-key": X_RAPIDAPI_KEY,
        }
        self.request = APIRequest()

    def search_videos_by_keywords(
        self, query: List[str], language: str, region: str
    ) -> Dict[str, Any]:
        params = f"keywords=%5B%22{'%22%2C%22'.join(query)}%22%5D&language={language}&region={region}"

        return self.request.post(self.base_url, params, self.headers)

    # def _get_converted_query(self, query: List[str]) -> str:
