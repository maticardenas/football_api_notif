from config.rapidapi import X_RAPIDAPI_HOST, X_RAPIDAPI_KEY

class BaseClient:
    def __init__(self) -> None:
        self.base_url = f"https://{X_RAPIDAPI_HOST}"
        self.headers = {
            'x-rapidapi-host': X_RAPIDAPI_HOST,
            'x-rapidapi-key': X_RAPIDAPI_KEY
        }