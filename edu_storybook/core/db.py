"""
db.py

Initializes the database connection.

Any error here is critical, and results in a halt of Flask app startup.
"""
from .config import config
from threading import Lock
import cx_Oracle
from . import sensitive
from .filepath import fix_filepath

import logging

c_db_log = logging.getLogger('core.db')
if config['production'] == False:
    c_db_log.setLevel(logging.DEBUG)

c_db_log.info('Connecting to database...')
oracle_lib_dir = None
with open(fix_filepath(__file__, config['sensitives']['files']['oracle_dir'])) as txtfile:
    for line in txtfile.readlines():
        oracle_lib_dir = str(line)
        break
assert oracle_lib_dir is not None and oracle_lib_dir != '', config['sensitives'][
    'folders']['oracle_dir'] + ' is empty, it needs the filepath to the Oracle Instant Client'

cx_Oracle.init_oracle_client(lib_dir=oracle_lib_dir)

oracle_configs = sensitive.oracle_config

connection = None
pool = None

def connect_db():
    '''
    Launch the connection to the database. This was moved to a function so that
    it can be called again if a `DPI-1010: not connected` error occurs.
    '''
    global connection
    global pool
    # hacky solution for Python relative importing
    # so that running this regularly and unit testing works
    corrected_connect_string = oracle_configs['connect_string'].replace(
        'data/Wallet_EDUStorybook',
        __file__.replace('db.py', '', 1) + 'data/Wallet_EDUStorybook',
        1 # replace once
    )
    c_db_log.debug('Corrected Oracle Wallet connect string is ' + corrected_connect_string)
    connection = cx_Oracle.connect(
        oracle_configs['username'],
        oracle_configs['password'],
        corrected_connect_string
    )

    pool = cx_Oracle.SessionPool(
        oracle_configs['username'],
        oracle_configs['password'],
        corrected_connect_string
    )
    pool.reconfigure(min=10, max=10, increment=0)
    pool.wait_timeout = 1000

connect_db()

c_db_log.info('Connected to database')

conn_lock = Lock()
