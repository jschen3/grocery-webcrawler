import logging

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
            "filename": "/opt/python/log/app.log",
            "formatter": "verbose",
        }
    },
    "loggers": {
        "root": {"handlers": ["applog"], "level": "DEBUG", "propagate": True}
    },
}


def info(message: str):
    logging.config.dictConfig(LOGGING_SETTINGS)
    logger = logging.getLogger(__name__)
    logger.info(message)


def debug(message: str):
    logging.config.dictConfig(LOGGING_SETTINGS)
    logger = logging.getLogger(__name__)
    logger.info(message)
