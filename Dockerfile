FROM python:3.9-bullseye
WORKDIR /code
RUN apt-get update && apt-get install -y cron python3-venv python3-pip nano
RUN apt-get install -y wget xvfb unzip
RUN apt-get install -y gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /chromedriver
COPY ./requirements.txt /code/requirements.txt


RUN python3 -m venv venv
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code
COPY ./mycrontab /code/mycrontab
COPY ./grocerywebcrawler.sh /code

RUN chmod +x /code/grocerywebcrawler.sh

RUN touch /var/log/cron.log
RUN crontab /code/mycrontab
EXPOSE 80
COPY ./startup.sh /code/startup.sh
RUN chmod +x ./startup.sh

WORKDIR /cronjob
COPY ./src /cronjob
COPY ./requirements.txt /cronjob
WORKDIR /code
CMD ["./startup.sh"]
