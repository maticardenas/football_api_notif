from config.telegram_notif import TOKEN
from src.api.telegram_client import TelegramClient


def send_telegram_message(
    chat_id: str, message: str = "", photo: str = "", video: str = ""
) -> None:
    telegram_client = TelegramClient(TOKEN)
    if photo:
        response = telegram_client.send_photo(chat_id, photo_url=photo, text=message)
    elif video:
        response = telegram_client.send_video(chat_id, video_url=video, text=message)
    else:
        response = telegram_client.send_message(chat_id, message)

    print(f"TELEGRAM MESSAGE SENT RESPONSE: {response.status_code}\n{response.text}")
