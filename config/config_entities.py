from dataclasses import dataclass


@dataclass
class TelegramRecipient:
    name: str
    telegram_id: str
    team_subscriptions: dict


@dataclass
class EmailRecipient:
    name: str
    email: str
