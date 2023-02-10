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
            "filename": "/var/log/app.log",
            "formatter": "verbose",
            "mode": "w"
        }
    },
    "loggers": {
        "root": {"handlers": ["applog"], "level": "DEBUG", "propagate": True}
    },
}


def info(message: str):
    log_filename = "/var/log/app.log"
    os.makedirs(os.path.dirname(log_filename), exist_ok=True)
    logging.config.dictConfig(LOGGING_SETTINGS)
    logger = logging.getLogger(__name__)
    logger.info(message)


def debug(message: str):
    log_filename = "/var/log/app.log"
    os.makedirs(os.path.dirname(log_filename), exist_ok=True)
    logging.config.dictConfig(LOGGING_SETTINGS)
    logger = logging.getLogger(__name__)
    logger.info(message)
