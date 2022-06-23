

# Football Telegram Bot

## Description

This application consumes, stores and processes football information and makes it available through a Telegram bot.

For adding this bot to telegram you should search it as `@card_football_bot`


## Main Functionalities

So far, it processes information about specific team's **fixtures**, informing past and future games.


## Bot Commands

- `/start` - Bot's introductory message.

- `/help` - Information about bot's commands and what they provide.

- `/available_teams` - Available team's that can be queried with the other commands.

- `/next_match <team>` - Retrieves information about next scheduled match for an specific team, including rival, date (in different timezones), league and round which is being played.

- `/last_match <team>` - Retrieves information about last match played by the specific team, including  scores, rival, date (in different timezones), league, roung and highlights

- `/today_matches` - Retrieves information about matches to be played on the current day.

- `/tomorrow_matches` - Retrieves information about matches to be played on the following day.

- `/last_played_matches` - Retrieves information about matches to be played on the previous day.


## Implementation Overview

Application is written in Python, as database engine uses PostgreSQL, jobs are scheduled using cronjob and it is finally deployed with Docker.

It consumes [RAPID API - API FOOTBALL](https://rapidapi.com/api-sports/api/api-football) endpoints, processes its data and stores it to the database. This runs in cronjobs scheduled, and then on demand user can request the processed team's information through Telegram's commands.


## Requirements

- Python 3.8+
- [Docker](https://www.docker.com/
- [Telegram Bot Token](https://core.telegram.org/bots)
