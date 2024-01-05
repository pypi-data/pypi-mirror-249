import logging
from logging.config import dictConfig

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(levelname)s - %(name)s: %(message)s",
            }
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
                "level": "DEBUG",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "log.log",
                "formatter": "default",
                "level": "DEBUG",
            },
            "info_file": {
                "class": "logging.FileHandler",
                "filename": "info.log",
                "formatter": "default",
                "level": "INFO",
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["stdout", "info_file"],
            "formatter": "default",
        },
    }
)


def getLogger(name: str):
    return logging.getLogger(name)
