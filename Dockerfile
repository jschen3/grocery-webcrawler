FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./src /code
CMD ["gunicorn", "webserver.app:app","-b","0.0.0.0:80","-k","uvicorn.workers.UvicornWorker"]