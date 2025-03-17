


from logging import INFO
from pathlib import Path
from app_config import AppConfig
from ficha import Ficha
from logging_service import LoggingService
from secret_key_generator import SecretKeyGenerator

class Api:
    def __init__(self, store_dir=None, logging_level=INFO):
        self.config = AppConfig(store_dir, logging_level)
        self.setup_store_files()
        self.logging_svc = LoggingService(self.config)
        self.logger = self.logging_svc.get_logger('Ficha_Api')
        self.gen = SecretKeyGenerator(self.config, self.logging_svc)
        self.ficha = Ficha(self.config, self.logging_svc)

    def setup_store_files(self):
        Path(self.config.store_dir).mkdir(parents=True, exist_ok=True)
        # self.logger.info(f'Store directory created successfully.')
        
    def add_key(self):
        self.gen.generate()

    def get_ficha(self):
        return self.ficha


def get_api(store_dir=None, logging_level=INFO):
    return Api(store_dir, logging_level)