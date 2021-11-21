cd /usr/football_api
/usr/local/bin/python -m pipenv shell
# PSG
/usr/local/bin/python -m pipenv run python /usr/football_api/team_fixture_notifier.py 2021 85 line_up_update
/usr/local/bin/python -m pipenv run python /usr/football_api/team_fixture_notifier.py 2022 85 line_up_update
# River
/usr/local/bin/python -m pipenv run python /usr/football_api/team_fixture_notifier.py 2021 435 line_up_update
/usr/local/bin/python -m pipenv run python /usr/football_api/team_fixture_notifier.py 2022 435 line_up_update
# Argentina
/usr/local/bin/python -m pipenv run python /usr/football_api/team_fixture_notifier.py 2021 26 line_up_update
/usr/local/bin/python -m pipenv run python /usr/football_api/team_fixture_notifier.py 2022 26 line_up_update