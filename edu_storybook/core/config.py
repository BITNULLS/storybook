"""
config.py

Just loads the configuration file (`data/config.json`) in.
"""

from .filepath import fix_filepath
import json
import os

with open(fix_filepath(__file__, 'data/config.json')) as jsonfile:
    config = json.load(jsonfile)
assert config is not None, 'Could not find ../config/config.json file.'

temp_folder = os.path.join( os.path.dirname(os.path.realpath(__file__)), config['temp_folder'] )
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)


class Config:
    '''
    This Config class just holds references to `config` where the are actually 
    loaded and initialized.

    This class will help type safety, and make it easier for our contributors.
    '''
    production: bool = config['production']
    domain: str = config['domain']
    last_mod: str = config['last_mod']
    login_duration: int = config['login_duration']
    buffer_size: int = config['buffer_size']
    temp_folder: str = config['temp_folder']
    temp_file_expire: int = config['temp_file_expire']
