FROM --platform=linux/amd64 python:3.9.6-bullseye

## Cron Job
# Chrome Installation
RUN apt-get update && apt-get install -y cron python3-venv python3-pip nano supervisor vim
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update -qqy --no-install-recommends && apt-get install -qqy --no-install-recommends google-chrome-stable

WORKDIR /cronjob
COPY ./src /cronjob
COPY ./requirements.txt /cronjob/requirements.txt
COPY .env /cronjob/.env
RUN touch /var/log/webcrawl705.log
RUN touch /var/log/webcrawl767.log
RUN touch /var/log/webcrawl1465.log
RUN touch /var/log/webcrawl1682.log
RUN touch /var/log/webcrawl2887.log
RUN touch /var/log/webcrawl2948.log
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
COPY ./webcrawlers_bash/grocerywebcrawler705.sh /code
COPY ./webcrawlers_bash/grocerywebcrawler767.sh /code
COPY ./webcrawlers_bash/grocerywebcrawler1465.sh /code
COPY ./webcrawlers_bash/grocerywebcrawler1682.sh /code
COPY ./webcrawlers_bash/grocerywebcrawler2887.sh /code
COPY ./webcrawlers_bash/grocerywebcrawler2948.sh /code
COPY ./price_calculate.sh /code
COPY ./clear_price_change_object.sh /code
RUN chmod +x /code/grocerywebcrawler705.sh
RUN chmod +x /code/grocerywebcrawler767.sh
RUN chmod +x /code/grocerywebcrawler1465.sh
RUN chmod +x /code/grocerywebcrawler1682.sh
RUN chmod +x /code/grocerywebcrawler2887.sh
RUN chmod +x /code/grocerywebcrawler2948.sh
RUN chmod +x /code/price_calculate.sh
RUN chmod +x /code/clear_price_change_object.sh
RUN crontab /code/mycrontab


### UI
RUN mkdir -p /etc/supervisor/conf.d
RUN apt-get install -y ca-certificates curl gnupg
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN apt-get install nodejs -y
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