import random
from typing import List

from config.covid_config import COVID_COUNTRIES
from config.email_notif import EMAIL_RECIPIENTS
from config.telegram_notif import TELEGRAM_RECIPIENTS
from src.emojis import Emojis
from src.entities import CovidStats
from src.senders.email_sender import send_email_html
from src.senders.telegram_sender import send_telegram_message
from src.utils.covid_utils import get_country_stats
from src.utils.fixtures_utils import get_image_search


class CovidManager:
    def notify_daily_stats(self):
        stats = []

        for country in COVID_COUNTRIES:
            country_stats = get_country_stats(country)
            stats.append(country_stats)

        self.perform_stats_notification(stats)

    def perform_stats_notification(self, stats: List[CovidStats]):
        covid_image_url = get_image_search(
            f"COVID in {random.choice([covid_stat.country.name for covid_stat in stats])}"
        )

        telegram_message = f"{Emojis.MICROBE.value} Datos de COVID-19 del día: \n\n"

        for stat in stats:
            telegram_message += f"{str(stat)}\n\n"

        for recipient in TELEGRAM_RECIPIENTS:
            send_telegram_message(
                TELEGRAM_RECIPIENTS[recipient],
                telegram_message,
                covid_image_url,
            )

        covid_image_text = f"<img src='{covid_image_url}'>"
        email_message = (
            f"{Emojis.MICROBE.value} Datos de COVID-19 del día:"
            f"<br /><br />{covid_image_text}<br /><br /> "
        )

        for stat in stats:
            email_message += f"{stat.email_like_repr()}<br /><br />"

        for recipient in EMAIL_RECIPIENTS:
            intro = f"Hola {recipient}! {Emojis.WAVING_HAND.value}<br /><br />"
            send_email_html(
                "Update diario - Covid-19",
                f"{intro}{email_message}",
                EMAIL_RECIPIENTS[recipient],
            )
