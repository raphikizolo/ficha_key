
from logging import INFO
import os


class AppConfig:
    def __init__(self, store_dir=None, logging_level=INFO):
        self.logging_level = logging_level
        self.store_dir = store_dir if store_dir else os.path.join(os.getenv('HOME'), '.ficha_key')
        self.log_file = os.path.join(self.store_dir, 'ficha_key.log')
        self.secret_key_file = os.path.join(self.store_dir, 'secret.key')
        self.backup_secret_keys_dir = os.path.join(self.store_dir, 'old_secret_keys_backup')