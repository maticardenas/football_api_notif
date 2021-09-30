from config.whatsapp_notif import RECIPIENTS
from src.api.fixtures_client import FixturesClient
from src.emojis import Emojis
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

        spanish_format_date = get_date_spanish_text_format(next_team_fixture.utc_date)

        for recipient in RECIPIENTS:
            message = f"{Emojis.WAVING_HAND.value}Hola {recipient}!\n\nTe recuerdo el proximo partido del PSG {Emojis.FRANCE.value}" \
                      f" de Lionel Messi {Emojis.GOAT.value}" \
                      f" es el {Emojis.SPIRAL_CALENDAR.value} {spanish_format_date}.\n\n{str(next_team_fixture)}"

            send_whatsapp_message(RECIPIENTS[recipient], message)
