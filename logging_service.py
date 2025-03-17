

import logging
from logging.handlers import RotatingFileHandler
import sys

from app_config import AppConfig


class LoggingService:
    def __init__(self, config: AppConfig):
        self.config = config
        self.LEVEL = config.logging_level
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.setLevel(self.LEVEL)
        self.file_handler = RotatingFileHandler(self.config.log_file, maxBytes=10_000_000_000_000, backupCount=3)
        self.file_handler.setLevel(config.logging_level)
        self.formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.file_handler.setFormatter(self.formatter)
        self.console_handler.setFormatter(self.formatter)

    def get_logger(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(self.config.logging_level)
        self.load_handlers(logger)
        return logger
    
    def load_handlers(self, logger):
        logger.addHandler(self.console_handler)
        logger.addHandler(self.file_handler)

        