#!/bin/bash
service cron start
exec uvicorn webserver.app:app --host 0.0.0.0 --port 80