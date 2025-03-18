import os
from pathlib import Path
import uuid
from cryptography.fernet import Fernet

from .app_config import AppConfig
from .logging_service import LoggingService


class SecretKeyGenerator:
    def __init__(self, app_config: AppConfig, logging_svc: LoggingService):
        self.config = app_config
        self.logger = logging_svc.get_logger(self.__class__.__name__)
        # self.make_directory()

    def check_old_secret_key_make_backup(self):
        if  os.path.isfile(self.config.secret_key_file) and Path(self.config.secret_key_file).stat().st_size:
            self.logger.debug(f'secret key exists. Creating a backup...')
            Path(self.config.backup_secret_keys_dir).mkdir(parents=True, exist_ok=True)
            with open(self.config.secret_key_file, 'rb') as f:
                old_key = f.read()
            old_s_key = os.path.join(self.config.backup_secret_keys_dir, f'secret_{uuid.uuid4()}.key')
            with open(old_s_key, 'wb') as sf:
                sf.write(old_key)

    def secret_key_exists(self):
        if not os.path.isfile(self.config.secret_key_file):
            return False
        with open(self.config.secret_key_file, 'rb') as f:
            return f.read().decode().strip() != ""

    def try_generate(self):
        "Checks if there's an existing secret key. Generates one if one does not exist."
        if not self.secret_key_exists():
            self.logger.debug('Secret key does not exist. Generating one...')
            self.generate(False)
            self.logger.debug('Generating secret key successful.')
            
    def generate(self, ask=True):
        "Generates a strong encryption secret key."
        c = input('Generate new secret key?Y/n ') if ask else 'y'
        if c.strip().lower() == 'y':
            key = Fernet.generate_key()
            # Save the key somewhere safe.
            self.check_old_secret_key_make_backup()
            with open(self.config.secret_key_file, "wb") as key_file:
                key_file.write(key)
            self.logger.info(f"Encryption key generated and saved as {self.config.secret_key_file}. Keep it safe!")
        

