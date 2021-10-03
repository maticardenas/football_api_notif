from config.email_notif import EMAIL_RECIPIENTS
from config.whatsapp_notif import RECIPIENTS
from src.api.fixtures_client import FixturesClient
from src.emojis import Emojis
from src.entities import Fixture
from src.senders.email_sender import send_email
from src.utils.date_utils import get_date_spanish_text_format
from src.utils.fixtures_utils import get_next_fixture
from src.senders.whatsapp_sender import send_whatsapp_message


class TeamFixturesManager:
    def __init__(self, season: int, team_id: int) -> None:
        self._season = season
        self._team_id = team_id
        self._fixtures_client = FixturesClient()

    def notify_next_fixture(self) -> None:
        team_fixtures = self._fixtures_client.get_fixtures_by(self._season, self._team_id)

        next_team_fixture = get_next_fixture(team_fixtures.as_dict["response"])

        if next_team_fixture.remaining_time().days < 3:
            self._perform_fixture_notification(next_team_fixture)

    @staticmethod
    def _perform_fixture_notification(team_fixture: Fixture) -> None:
        spanish_format_date = get_date_spanish_text_format(team_fixture.utc_date)
        date_text = f"es el {Emojis.SPIRAL_CALENDAR.value} {spanish_format_date}" \
                    if team_fixture.remaining_time().days > 0 else "es HOY!"

        for recipient in RECIPIENTS:
            message = f"{Emojis.WAVING_HAND.value}Hola {recipient}!\n\nTe recuerdo que el proximo partido del PSG {Emojis.FRANCE.value}" \
                      f" de Lionel Messi {Emojis.GOAT.value} {date_text}.\n\n{str(team_fixture)}"

            send_whatsapp_message(RECIPIENTS[recipient], message)

        for recipient in EMAIL_RECIPIENTS:
            message = f"{Emojis.WAVING_HAND.value}Hola {recipient}!\n\nTe recuerdo que el proximo partido del PSG {Emojis.FRANCE.value}" \
                      f" de Lionel Messi {Emojis.GOAT.value} {date_text}.\n\n{team_fixture.email_like_repr()}"

            send_email(f"{team_fixture.home_team} vs. {team_fixture.away_team}", message, EMAIL_RECIPIENTS[recipient])

