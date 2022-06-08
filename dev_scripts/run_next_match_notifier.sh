cd /usr/football_api
/usr/local/bin/python -m pipenv shell
# PSG
/usr/local/bin/python -m pipenv run python /usr/football_api/team_fixture_notifier.py 2021 85 next_match
/usr/local/bin/python -m pipenv run python /usr/football_api/team_fixture_notifier.py 2022 85 next_match
# River
/usr/local/bin/python -m pipenv run python /usr/football_api/team_fixture_notifier.py 2021 435 next_match
/usr/local/bin/python -m pipenv run python /usr/football_api/team_fixture_notifier.py 2022 435 next_match
# Argentina
/usr/local/bin/python -m pipenv run python /usr/football_api/team_fixture_notifier.py 2021 26 next_match
/usr/local/bin/python -m pipenv run python /usr/football_api/team_fixture_notifier.py 2022 26 next_match