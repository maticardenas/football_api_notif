cd /usr/football_api
/usr/local/bin/python -m pipenv shell

/usr/local/bin/python -m pipenv run python /usr/football_api/db_initializer.py

# PSG
/usr/local/bin/python -m pipenv run python /usr/football_api/db_populator.py 2021 85
/usr/local/bin/python -m pipenv run python /usr/football_api/db_populator.py 2022 85
# River
#/usr/local/bin/python -m pipenv run python /usr/football_api/db_populator.py 2022 435
## Argentina
#/usr/local/bin/python -m pipenv run python /usr/football_api/db_populator.py  2022 26
## Boke
#/usr/local/bin/python -m pipenv run python /usr/football_api/db_populator.py  2022 451
## Belgrano
#/usr/local/bin/python -m pipenv run python /usr/football_api/db_populator.py  2022 440