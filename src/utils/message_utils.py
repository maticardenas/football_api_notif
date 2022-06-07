from typing import List

from config.config_entities import TelegramRecipient
from src.emojis import Emojis

TEAMS_ALIASES = {"85": ["PSG"]}


def get_team_intro_messages(team_id: str, is_group_notification: bool = False) -> str:
    pronoun = "Les" if is_group_notification else "Te"
    first_phrase = "recuerdo que el próximo partido"
    switch = {
        "85": {
            "next_match": f"{pronoun} {first_phrase} del PSG {Emojis.FRANCE.value}"
            f" de Lionel Messi {Emojis.GOAT.value}",
            "last_match": f"El PSG {Emojis.FRANCE.value} de Lionel Messi {Emojis.GOAT.value}",
        },
        "435": {
            "next_match": f"{pronoun} {first_phrase} del River de Marcelo Gallardios",
            "last_match": f"El River de Marcelo Gallardios",
        },
        "26": {
            "next_match": f"{pronoun} {first_phrase} de La Scaloneta {Emojis.ARGENTINA.value}",
            "last_match": f"La Scaloneta {Emojis.ARGENTINA.value}",
        },
        "451": {
            "next_match": f"{pronoun} {first_phrase} de La Battaglieta {Emojis.BLUE_CIRCLE.value}{Emojis.YELLOW_CIRCLE.value}",
            "last_match": f"La Battaglieta {Emojis.BLUE_CIRCLE.value}{Emojis.YELLOW_CIRCLE.value}",
        },
        "440": {
            "next_match": f"{pronoun} {first_phrase} de Belgrano {Emojis.PIRATE_FLAG.value}",
            "last_match": f"Belgrano {Emojis.PIRATE_FLAG.value}",
        },
    }

    return switch.get(team_id)


def get_highlights_text(highlights: List[str], email: bool = False) -> str:
    endline = "<br />" if email else "\n"
    highlights_text = ""
    highlight_number = 1

    for highlight in highlights:
        highlights_text += f"{Emojis.FILM_PROJECTOR.value} <a href='{highlight}'>HIGHLIGHTS [{highlight_number}]</a>{endline}"
        highlight_number += 1

    return highlights_text


def is_subscripted_for_team(telegram_recipient: TelegramRecipient, team_id) -> bool:
    return team_id in telegram_recipient.team_subscriptions
