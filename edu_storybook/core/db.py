"""
db.py
    Initializes the database connection.
"""
from .config import config
from threading import Lock
import cx_Oracle
from . import sensitive

print('Connecting to database...', end=' ')
oracle_lib_dir = None
with open(config['sensitives']['files']['oracle_dir']) as txtfile:
    for line in txtfile.readlines():
        oracle_lib_dir = str(line)
        break
assert oracle_lib_dir is not None and oracle_lib_dir != '', config['sensitives'][
    'folders']['oracle_dir'] + ' is empty, it needs the filepath to the Oracle Instant Client'

cx_Oracle.init_oracle_client(lib_dir=oracle_lib_dir)

oracle_configs = sensitive.oracle_config

connection = cx_Oracle.connect(
    oracle_configs['username'],
    oracle_configs['password'],
    oracle_configs['connect_string']
)
print('connected')

conn_lock = Lock()
