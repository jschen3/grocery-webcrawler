FROM python:3.10-bullseye
WORKDIR /cronjob
COPY /requirements.txt ./requirements.txt
RUN apt-get update && apt-get install -y cron python3-venv python3-pip
COPY /src /cronjob/src
COPY /cronjob/grocerywebcrawler.sh ./grocerywebcrawler.sh
RUN chmod +x ./grocerywebcrawler.sh
COPY /cronjob/mycrontab ./mycrontab
RUN touch /var/log/cron.log
RUN crontab /cronjob/mycrontab
CMD cron && tail -f /var/log/cron.log