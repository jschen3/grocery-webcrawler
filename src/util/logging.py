import logging
import os

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
            "filename": "/opt/python/logs/app.log",
            "formatter": "verbose",
            "mode": "a"
        }
    },
    "loggers": {
        "root": {"handlers": ["applog"], "level": "DEBUG", "propagate": True}
    },
}


def info(message: str):
    if not os.path.exists("opt/python/logs/"):
        os.makedirs("opt/python/logs/")
    logging.config.dictConfig(LOGGING_SETTINGS)
    logger = logging.getLogger(__name__)
    logger.info(message)


def debug(message: str):
    if not os.path.exists("opt/python/logs/"):
        os.makedirs("opt/python/logs/")
    logging.config.dictConfig(LOGGING_SETTINGS)
    logger = logging.getLogger(__name__)
    logger.info(message)
