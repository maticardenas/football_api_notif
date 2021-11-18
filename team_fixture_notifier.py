#!/bin/env python
import sys

from src.team_fixtures_manager import TeamFixturesManager

if __name__ == "__main__":
    season = sys.argv[1]
    team = sys.argv[2]
    notif_type = sys.argv[3]

    team_fixtures_manager = TeamFixturesManager(season, team)

    if notif_type == "next_match":
        team_fixtures_manager.notify_next_fixture()
    else:
        team_fixtures_manager.notify_last_fixture()
