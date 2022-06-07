import json
from pathlib import Path
from typing import Any, Dict, List

from config.config_entities import TelegramRecipient, EmailRecipient

TELEGRAM_RECIPIENTS_FILE = Path(__file__).parent.absolute() / "telegram_recipients.json"
EMAIL_RECIPIENTS_FILE = Path(__file__).parent.absolute() / "email_recipients.json"


def get_json_file_data(file_path: Path) -> Dict[str, Any]:
    with open(file_path, mode="r") as f:
        return json.load(f)


def get_telegram_recipients_config() -> List[TelegramRecipient]:
    json_file_data = get_json_file_data(TELEGRAM_RECIPIENTS_FILE)
    return [
        TelegramRecipient(
            telegram_recipient["name"],
            telegram_recipient["telegram_id"],
            telegram_recipient["team_subscriptions"],
        )
        for telegram_recipient in json_file_data
    ]


def get_email_recipients_config() -> List[EmailRecipient]:
    json_file_data = get_json_file_data(EMAIL_RECIPIENTS_FILE)
    return [
        EmailRecipient(email_recipient["name"], email_recipient["email"])
        for email_recipient in json_file_data
    ]
