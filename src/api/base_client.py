from config.notif_config import NotifConfig


class BaseClient:
    def __init__(self) -> None:
        self.base_url = f"https://{NotifConfig.X_RAPIDAPI_HOST}"
        self.headers = {
            "x-rapidapi-host": NotifConfig.X_RAPIDAPI_HOST,
            "x-rapidapi-key": NotifConfig.X_RAPIDAPI_KEY,
        }
