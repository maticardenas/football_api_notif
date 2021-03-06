FROM python:3.8

LABEL maintainer "Matias Cardenas"
LABEL description "Python 3.8 image containing Football Notifications APP"

USER root
RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean \
&& apt-get install cron -y \
&& apt-get install bash \
&& apt-get install vim -y

ADD football_notif_crontab /etc/cron.d/football_notif_crontab
RUN chmod 777 /etc/cron.d/football_notif_crontab
RUN crontab /etc/cron.d/football_notif_crontab
RUN touch /var/log/cron_log.log
RUN pip install pipenv

WORKDIR /usr/football_api

COPY ./config ./config
COPY ./dev_scripts ./dev_scripts
COPY ./src ./src
COPY ./tests ./tests
COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock
COPY team_fixture_notifier.py .
COPY db_initializer.py .
COPY db_populator.py .
COPY head_to_head_updater.py .
COPY notifier_bot.py .
COPY football_notifier.env .
COPY partial_db_updater.py .

RUN cat football_notifier.env >> /etc/environment

RUN python -m pipenv install

CMD cron && tail -f /var/log/cron_log.log
