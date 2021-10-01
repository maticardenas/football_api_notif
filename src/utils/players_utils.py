from typing import Dict, Any

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


def get_all_player_stats(player_response, team_filter: str) -> str:
    player_details = player_response["player"]
    player_summary = get_str_player_summary(player_details)

    messi_stats = convert_player_stats(player_response)
    stats_summary = get_str_stats_summary(messi_stats, team_filter)

    return f"{player_summary}\n\n_Statistics:_\n\n{stats_summary}"


def get_str_player_summary(player_details: Dict[str, Any]) -> str:
    return f"_Player:_ *{player_details['firstname']} {player_details['lastname']}*\n" \
                     f"_Age:_ *{player_details['age']}*\n" \
                     f"_Nationality:_ *{player_details['nationality']}*\n" \
                     f"_Height:_ *{player_details['height']}*\n" \
                     f"_Weight:_ *{player_details['weight']}*\n" \
                     f"_Photo:_ *{player_details['photo']}*"


def get_str_stats_summary(stats: Dict[str, PlayerStats], team_filter: str) -> str:
    player_stats = ""
    for team in stats:
        if team_filter:
            if team.lower() != team_filter.lower():
                continue
        for championship in stats[team]:
            player_stats += f"_Team:_ *{team}* - Championship: *{championship}*\n{str(stats[team][championship])}\n\n"

    return player_stats
