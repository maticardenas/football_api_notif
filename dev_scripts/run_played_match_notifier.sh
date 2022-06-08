cd /usr/football_api
/usr/local/bin/python -m pipenv shell
# PSG
/usr/local/bin/python -m pipenv run python /usr/football_api/team_fixture_notifier.py 2021 85 played_match
/usr/local/bin/python -m pipenv run python /usr/football_api/team_fixture_notifier.py 2022 85 played_match
# River
/usr/local/bin/python -m pipenv run python /usr/football_api/team_fixture_notifier.py 2021 435 played_match
/usr/local/bin/python -m pipenv run python /usr/football_api/team_fixture_notifier.py 2022 435 played_match
# Argentina
/usr/local/bin/python -m pipenv run python /usr/football_api/team_fixture_notifier.py 2022 26 played_match