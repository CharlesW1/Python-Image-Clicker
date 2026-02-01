import logging
from .config import LOG_FILE, LOG_LEVEL


def setup_logging():
    logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL,
                        format='%(asctime)s - %(levelname)s: %(message)s')
    return logging


def get_logger(name=__name__):
    setup_logging()
    return logging.getLogger(name)
