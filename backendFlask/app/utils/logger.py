import logging
from logging.handlers import RotatingFileHandler
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
LOG_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, "logs"))
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name, filename):
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(
        os.path.join(LOG_DIR, filename),
        maxBytes=5_000_000,
        backupCount=5
    )
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


