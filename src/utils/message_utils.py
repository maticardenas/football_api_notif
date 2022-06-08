from src.emojis import Emojis


def get_team_intro_messages(team_id: str, is_group_notification: bool = False) -> str:
    pronoun = "Les" if is_group_notification else "Te"
    switch = {
        "85": {
            "next_match": f"{pronoun} recuerdo que el próximo partido del PSG {Emojis.FRANCE.value}"
            f" de Lionel Messi {Emojis.GOAT.value}",
            "last_match": f"El PSG {Emojis.FRANCE.value} de Lionel Messi {Emojis.GOAT.value}",
        },
        "435": {
            "next_match": f"{pronoun} recuerdo que el próximo partido del River de Marcelo Gallardios",
            "last_match": f"El River de Marcelo Gallardios",
        },
        "26:": {
            "next_match": f"{pronoun} recuerdo que el próximo partido de La Scaloneta {Emojis.ARGENTINA.value}",
            "last_match": f"La Scaloneta {Emojis.ARGENTINA.value}",
        },
    }

    return switch.get(team_id)
