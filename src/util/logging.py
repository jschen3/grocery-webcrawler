import logging
import os
from pathlib import Path

LOGGING_SETTINGS = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(asctime)s %(levelname)s %(module)s: %(message)s"}
    },
    "handlers": {
        "applog": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "/var/log/app.log",
            "formatter": "verbose",
            "mode": "a+"
        }
    },
    "loggers": {
        "root": {"handlers": ["applog"], "level": "DEBUG", "propagate": True}
    },
}


def info(message: str):
    os.makedirs(os.path.dirname("/var/log/app.log"), exist_ok=True)
    logging.config.dictConfig(LOGGING_SETTINGS)
    logger = logging.getLogger(__name__)
    logger.info(message)


def debug(message: str):
    os.makedirs(os.path.dirname("var/log/app.log"), exist_ok=True)
    logging.config.dictConfig(LOGGING_SETTINGS)
    logger = logging.getLogger(__name__)
    logger.info(message)
