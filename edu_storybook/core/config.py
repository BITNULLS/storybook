"""
config.py
    Just loads the configuration file in.
"""

from .helper import fix_filepath
import json

with open(fix_filepath(__file__, 'data/config.json')) as jsonfile:
    config = json.load(jsonfile)
assert config is not None, 'Could not find ../config/config.json file.'
