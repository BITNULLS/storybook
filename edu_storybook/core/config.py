"""
config.py
    Just loads the configuration file in.
"""

from .helper import fix_filepath
import json
import os

with open(fix_filepath(__file__, 'data/config.json')) as jsonfile:
    config = json.load(jsonfile)
assert config is not None, 'Could not find ../config/config.json file.'

temp_folder = os.path.join( os.path.dirname(os.path.realpath(__file__)), config['temp_folder'] )
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)