from datetime import datetime
import json
from logging import DEBUG
import os
import ficha_key.api
from ficha_key.app_config import AppConfig

# continue from here.

# create tests for ficha on the following features.
# creation of new key.
# encryption
# decryption
# encryption and decryption on adding new keys while backing up the old one.
# key deletion


def ensure_key_replaced(config: AppConfig, old_key, logger):
    with open(config.secret_key_file) as f:
        ck = f.read()
        if (not ck) or ck == old_key:
            logger.debug('Key replacement failed.')
        else:
            logger.debug('Key replacement successfull.')

def get_current_key(config: AppConfig):
    with open(config.secret_key_file) as f:
        return f.read()
    

def get_timestamp():
    return datetime.now().strftime('%d/%m/%Y-%H:%M:%S')

def ensure_decrypted(key, value, encrypted_data_file, logger):
    if os.path.isfile(encrypted_data_file):
        with open(encrypted_data_file) as f:
            data = f.read()
            try:
                m = json.loads(data)
                logger.debug('Encryption failed. Data file has unencrypted data.')
            except:
                logger.debug('Encryption successful.')

if __name__ == "__main__":
    test_store_dir = os.path.join(os.curdir, 'test_store_dir')
    encr_svc = ficha_key.api.get_api(test_store_dir, DEBUG)
    logger = encr_svc.logging_svc.get_logger(f'Tests-of-time-[{get_timestamp()}]')
    logger.debug('Tests starting...')
    old_key = get_current_key(encr_svc.config)
    encr_svc.add_key()
    ensure_key_replaced(encr_svc.config, old_key, logger)

    data_file = os.path.join(os.getcwd(), 'data_file.txt')
    token_name, token = 'api 1 token', 'farwerer392484239y5fdofjeroe-re1234u3rehiufdfndjkferehregrgn;rretkjltteritj4oroerjwq'
    ficha = encr_svc.get_ficha()
    ficha.encrypt(token_name, token, data_file)
    ensure_decrypted(token_name, token, data_file, logger)
    stored_token = ficha.get_stored_token(token_name, data_file)
    if stored_token == token:
        logger.debug('Decryption is working as expected.')
    else:
        logger.debug('Decryption failed.')
    logger.debug('Tests finished...')

