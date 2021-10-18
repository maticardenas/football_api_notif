from typing import Any, Dict

from src.api.base_client import BaseClient
from src.request import APIRequest

class TelegramClient(BaseClient):
    def __init__(self, token: str) -> None:
        super().__init__()
        self._token = token
        self.base_url = "https://api.telegram.org"
        self.endpoint = f"/bot{self._token}/sendMessage"
        self.request = APIRequest()

    def send_message(self, chat_id: str, msg: str) -> Dict[str, Any]:
        params = {
            "chat_id": chat_id,
            "text": msg,
            "parse_mode": "markdown"
        }
        url = f"{self.base_url}{self.endpoint}"

        return self.request.post(url, params, self.headers)