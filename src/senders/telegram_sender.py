from config.telegram_notif import TOKEN, CHAT_ID
from src.api.telegram_client import TelegramClient

def send_telegram_message(message: str) -> None:
   telegram_client = TelegramClient(TOKEN)
   telegram_client.send_message(CHAT_ID, message)
