import logging


def info(message: str):
    logging.basicConfig(filename="/opt/python/log/app.log", format='%(asctime)s-%(process)d-%(levelname)s %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info(message)

def debug(message: str):
    logging.basicConfig(filename="/opt/python/log/app.log", format='%(asctime)s-%(process)d-%(levelname)s %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=logging.DEBUG)

    logger = logging.getLogger(__name__)
    logger.debug(message)