FROM python:3.8

LABEL maintainer "Matias Cardenas"
LABEL description	"Python 3.8 image containing Football Notifications APP"

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

RUN pip install pipenv
WORKDIR /usr/football_api

COPY ./config ./config
COPY ./dev_scripts ./dev_scripts
COPY ./src ./src
COPY ./tests ./tests
COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock
COPY main.py .

RUN cd /usr/football_api
RUN python -m pipenv install
