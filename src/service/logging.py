import logging

from src.config import Config


def set_logging(config: Config):
    logging.basicConfig(
        level=config.logging.level,
        format=config.logging.format,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(config.logging.file, encoding='utf-8')
        ]
    )
