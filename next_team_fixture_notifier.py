#!/bin/env python
import sys

from src.senders.whatsapp_sender import send_whatsapp_message
from src.team_fixtures_manager import TeamFixturesManager

if __name__ == "__main__":
    season = sys.argv[1]
    team = sys.argv[2]

    team_fixtures_manager = TeamFixturesManager(season, team)
    team_fixtures_manager.notify_next_fixture()
