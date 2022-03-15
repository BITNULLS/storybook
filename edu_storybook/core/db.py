"""
db.py
    Initializes the database connection.
"""
from .config import config
from threading import Lock
import cx_Oracle
from . import sensitive
from .filepath import fix_filepath

import logging 

logging.info('Connecting to database...')
oracle_lib_dir = None
with open(fix_filepath(__file__, config['sensitives']['files']['oracle_dir'])) as txtfile:
    for line in txtfile.readlines():
        oracle_lib_dir = str(line)
        break
assert oracle_lib_dir is not None and oracle_lib_dir != '', config['sensitives'][
    'folders']['oracle_dir'] + ' is empty, it needs the filepath to the Oracle Instant Client'

cx_Oracle.init_oracle_client(lib_dir=oracle_lib_dir)

oracle_configs = sensitive.oracle_config

# hacky solution for Python relative importing
# so that running this regularly and unit testing works
corrected_connect_string = oracle_configs['connect_string'].replace(
    'data/Wallet_EDUStorybook', 
    __file__.replace('db.py', '', 1) + 'data/Wallet_EDUStorybook', 
    1 # replace once
)

logging.debug('Corrected Oracle Wallet connect string is ' + corrected_connect_string)

connection = cx_Oracle.connect(
    oracle_configs['username'],
    oracle_configs['password'],
    corrected_connect_string
)

logging.info('Connected to database')

conn_lock = Lock()
