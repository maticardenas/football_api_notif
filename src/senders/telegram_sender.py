from config.telegram_notif import TOKEN
from src.api.telegram_client import TelegramClient


def send_telegram_message(chat_id: str, message: str) -> None:
    telegram_client = TelegramClient(TOKEN)
    telegram_client.send_message(chat_id, message)
