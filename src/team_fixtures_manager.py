from config.whatsapp_notif import RECIPIENTS
from src.api.fixtures_client import FixturesClient
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

        for recipient in RECIPIENTS:
            message = f"Hola {recipient}!\nTe recuerdo el proximo partido del PSG de Lionel Messi:\n\n{str(next_team_fixture)}"
            send_whatsapp_message(RECIPIENTS[recipient], message)
