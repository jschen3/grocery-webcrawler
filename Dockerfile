FROM python:3.10-bullseye
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apt-get update && apt-get install -y cron python3-venv python3-pip
COPY ./src /code
COPY ./grocerywebcrawler.sh /code/grocerywebcrawler.sh
RUN chmod +x /code/grocerywebcrawler.sh
COPY ./mycrontab /code/mycrontab
RUN touch /var/log/cron.log
RUN crontab /code/mycrontab
RUN cron
WORKDIR /app
RUN python3 -m venv venv
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src /app
CMD ["uvicorn", "webserver.app:app","--host","0.0.0.0","--port","80"]