FROM python:3.10.10-bullseye

## Cron Job
# Chrome Installation
RUN apt-get update && apt-get install -y cron python3-venv python3-pip nano supervisor vim
RUN apt-get install -y gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /chromedriver

WORKDIR /cronjob
COPY ./src /cronjob
COPY ./requirements.txt /cronjob/requirements.txt
COPY .env /cronjob/.env
RUN touch /var/log/webcrawl.log
RUN touch /var/log/pricecalculate.log
RUN touch /var/log/cron.log

### Uvicorn Server
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
COPY .env /code/.env
RUN python3 -m venv venv
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./src /code
EXPOSE 5000


### Run Scripts
COPY ./mycrontab /code/mycrontab
COPY ./grocerywebcrawler705.sh /code
COPY ./grocerywebcrawler767.sh /code
COPY ./grocerywebcrawler1465.sh /code
COPY ./grocerywebcrawler1682.sh /code
COPY ./grocerywebcrawler2887.sh /code
COPY ./grocerywebcrawler2948.sh /code
COPY ./increment_counter.sh /code
COPY ./price_calculate.sh /code
RUN chmod +x /code/grocerywebcrawler705.sh
RUN chmod +x /code/grocerywebcrawler767.sh
RUN chmod +x /code/grocerywebcrawler1465.sh
RUN chmod +x /code/grocerywebcrawler1682.sh
RUN chmod +x /code/grocerywebcrawler2887.sh
RUN chmod +x /code/grocerywebcrawler2948.sh
RUN chmod +x /code/increment_counter.sh
RUN chmod +x /code/price_calculate.sh
RUN crontab /code/mycrontab


### UI
RUN mkdir -p /etc/supervisor/conf.d
RUN curl -fsSL https://deb.nodesource.com/setup_19.x | bash - &&\
apt-get install -y nodejs
WORKDIR /frontend
COPY ./grocerywebsite/package.json /frontend/package.json
COPY ./grocerywebsite/package-lock.json /frontend/package-lock.json
COPY ./grocerywebsite/playwright.config.ts /frontend/playwright.config.ts
COPY ./grocerywebsite/svelte.config.js /frontend/svelte.config.js
COPY ./grocerywebsite/tsconfig.json /frontend/tsconfig.json
COPY ./grocerywebsite/vite.config.js /frontend/vite.config.js
COPY ./grocerywebsite/src /frontend/src
COPY ./grocerywebsite/static /frontend/static
COPY ./grocerywebsite/tests /frontend/tests
RUN npm --prefix /frontend install
RUN npm --prefix /frontend run build
EXPOSE 80
WORKDIR /code


### Supervisor

COPY supervisor.conf /etc/supervisor.conf
CMD ["supervisord", "-c", "/etc/supervisor.conf"]