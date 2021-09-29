
from fixtures_email import send_email
from src.api.fixtures_client import FixturesClient
from src.fixtures_utils import get_next_fixture

if __name__ == "__main__":
    fixtures_client = FixturesClient()

    psg_fixtures_response = fixtures_client.get_fixtures_by(2021, 85)

    psg_next_fixture = get_next_fixture(psg_fixtures_response.as_dict["response"])

    body = str(psg_next_fixture)

    send_email("Prox Partido PSG notif (python) tests", body)
