from typing import Dict, Any

from src.api.players_client import PlayersClient
from src.entities import PlayerStats


def convert_player_stats(stats_response: Dict[str, Any]) -> Dict[str, PlayerStats]:
    player_stats = {}

    for stats in stats_response["statistics"]:
        team = stats["team"]["name"]
        championship = stats["league"]["name"]

        champs_stats = {
            championship: PlayerStats(
                stats["games"]["appearences"],
                stats["games"]["minutes"],
                stats["shots"]["total"],
                stats["shots"]["on"],
                stats["goals"]["total"],
                stats["passes"]["total"],
                stats["passes"]["key"],
                stats["passes"]["accuracy"],
                stats["dribbles"]["attempts"],
                stats["dribbles"]["success"],
            )
        }

        if team not in player_stats:
            player_stats[team] = champs_stats
        else:
            player_stats[team].update(champs_stats)

    return player_stats


def get_all_player_stats() -> str:
    players_client = PlayersClient()

    messi_stats_response = players_client.get_players_stats_by(2021, 154)

    first_response = messi_stats_response.as_dict["response"][0]
    player_details = first_response["player"]
    player_summary = get_str_player_summary(player_details)

    messi_stats = convert_player_stats(first_response)
    stats_summary = get_str_stats_summary(messi_stats)

    return f"{player_summary}\n\nStatistics:\n{stats_summary}"


def get_str_player_summary(player_details: Dict[str, Any]) -> str:
    return f"Player: {player_details['firstname']} {player_details['lastname']}\n " \
                     f"Age: {player_details['age']}\n" \
                     f"Nationality: {player_details['nationality']}\n" \
                     f"Height: {player_details['height']}\n " \
                     f"Weight: {player_details['weight']}\n " \
                     f"Photo: {player_details['photo']}"


def get_str_stats_summary(stats: Dict[str, PlayerStats]) -> str:
    player_stats = ""
    for team in stats:
        for championship in stats[team]:
            player_stats += f"Team: {team} - Championship: {championship}\n{str(stats[team][championship])}\n\n"

    return player_stats
