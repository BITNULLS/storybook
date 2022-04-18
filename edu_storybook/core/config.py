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
    '''
    True means live website, false means development mode
    '''

    domain: str = config['domain']
    '''
    The domain where this application will be hosted on. Must not have a
    trailing slash.
    '''

    last_mod: str = config['last_mod']
    '''
    YYYY-MM-DD of last modification made to project
    '''

    login_duration: int = config['login_duration']
    '''
    How many seconds can a user login for before needing to sign in again
    '''

    buffer_size: int = config['buffer_size']
    '''
    The size of file reading buffer
    '''

    temp_folder: str = config['temp_folder']
    '''
    Where our temporary files will be saved
    '''

    temp_file_expire: int = config['temp_file_expire']
    '''
    How many seconds minimum to keep a temporary download file on the server
    '''

    jwt_alg: str = config['jwt_alg']
    '''
    Which JWT (JSON Web Token) algorithm are we using to encrypt our tokens
    '''

