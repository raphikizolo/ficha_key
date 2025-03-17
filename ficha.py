import json
import os
import cryptography
import cryptography.exceptions
from cryptography.fernet import Fernet
import cryptography.fernet

from app_config import AppConfig
from logging_service import LoggingService


class Ficha:
    def __init__(self, config: AppConfig, logging_svc: LoggingService):
        self.config = config
        self.logger = logging_svc.get_logger(self.__class__.__name__)

    def get_cipher(self, secret_key_file=None):
        with open(secret_key_file if secret_key_file else self.config.secret_key_file, "rb") as key_file:
            key = key_file.read()
        
        return Fernet(key)
    
    def encrypt(self, json_key, json_value, encrypted_data_file):
        cipher = self.get_cipher()
        decrypted_data = self.decrypt(encrypted_data_file, cipher).decode()
        data = json.loads(decrypted_data) if decrypted_data else {}
        data[json_key] = json_value
        json_data = json.dumps(data).encode()
        encrypted = cipher.encrypt(json_data)
        with open(encrypted_data_file, 'wb') as f:
            f.write(encrypted)

    def decryptd(self, encrypted_data_file, cipher: Fernet=None, secret_key_file=None, try_with_old_keys=True):
        "Decrypts and returns the data as a dictionary"
        return json.loads(self.decrypt(encrypted_data_file, cipher, secret_key_file, try_with_old_keys))

    def decrypt(self, encrypted_data_file, cipher: Fernet=None, secret_key_file=None, try_with_old_keys=True):
        try:
            cipher = cipher if cipher else self.get_cipher(secret_key_file)
            with open(encrypted_data_file, 'rb') as enc_file:
                encrypted_data = enc_file.read()
                return cipher.decrypt(encrypted_data) if encrypted_data else b''
        except cryptography.fernet.InvalidToken:
            self.logger.debug(f'Decryption failed. Probably invalid secret key. ' + ('Attempting to decrypt using backed up keys...' if try_with_old_keys else ''))
            if try_with_old_keys:
                for dir, _, files  in os.walk(self.config.backup_secret_keys_dir):
                    old_key_files = [os.path.join(dir, f) for f in files if f.endswith('.key')]
                    for old_key_file in old_key_files:
                        try:
                            data = self.decrypt(encrypted_data_file, None, old_key_file, False)
                            self.delete_old_key(old_key_file)
                            return data
                        except Exception as e:                        
                            self.logger.debug(f'Decryption with old key failed. Details {"[-]".join(e.args)}')
        raise Exception(f'Decryption failed. See log for more details. Log is here -> {self.config.log_file}')
    
    def delete_old_key(self, old_key_file):
        os.remove(old_key_file)
        self.logger.debug('Removed old secret key file.')

    
    def get_stored_token(self, key, encrypted_tokens_file):
        m = self.decryptd(encrypted_tokens_file)
        return m[key] if key in m else None
