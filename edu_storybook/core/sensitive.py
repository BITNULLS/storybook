"""
sensitive.py

Downloads, loads in, and then deletes all sensitive data files.
Any error here is critical, and should stop execution of the app.

The following behaviors are implemented:
 - Unzip Oracle wallet
 - Get domain name
 - Log into email client
 - Initialize `jwt_key`
 - Setup Oracle login info (Oracle Key)
"""

import logging
import json
import smtplib
import ssl

from .filepath import fix_filepath
from . import bucket
import os
from zipfile import ZipFile
from .config import config

c_sensitive_log = logging.getLogger('core.sensitive')

if config['production'] == False:
    c_sensitive_log.setLevel(logging.DEBUG)

# Unzip Wallet
c_sensitive_log.debug('Unzipping wallet...')
wallet_zip_path = fix_filepath(__file__, 'data/Wallet_EDUStorybook')

if not os.path.isdir(wallet_zip_path):
    os.mkdir(wallet_zip_path)
with ZipFile(bucket.wallet, 'r') as zip_ref:
    zip_ref.extractall(wallet_zip_path)
os.remove(bucket.wallet)

c_sensitive_log.debug('Wallet unzipped, extracted, and removed')

# Get Domain Name
c_sensitive_log.debug('Reading domain name...')
domain_name = None
with open(bucket.domain) as txtfile:
    for line in txtfile.readlines():
        domain_name = str(line)
        break
os.remove(bucket.domain)
assert domain_name is not None and domain_name != '', config['sensitives'][
    'files']['domain_name'] + ' is empty; It should not be empty'

c_sensitive_log.debug('Domain read in')

# email login
c_sensitive_log.debug('Logging into email account...')
with open(bucket.email) as email_config:
    email_login = json.load(email_config)
    email_password = email_login['password']
os.remove(bucket.email)

try:
    smtp = 'smtp.gmail.com'
    port = 587
    context = ssl.create_default_context()
    server = smtplib.SMTP(smtp, port)
    server.starttls(context=context)
    server.login('edustorybooks@gmail.com', email_password)
except Exception as e:
    c_sensitive_log.warning("Email Server Error")
    c_sensitive_log.warning(e)
else:
    c_sensitive_log.debug('Logged into email account')

# jwt_key Initialization
c_sensitive_log.debug('Loading in jwt_key...')
with open(bucket.jwt) as txtfile:
    for line in txtfile.readlines():
        jwt_key = str(line)
        break
os.remove(bucket.jwt)
c_sensitive_log.debug('jwt_key loaded in')

# Oracle Key Set up
c_sensitive_log.debug('Loading in Oracle Key...')
with open(bucket.oracle_key) as jsonfile:
    oracle_config = json.load(jsonfile)
os.remove(bucket.oracle_key)
assert oracle_config is not None, 'Oracle Key json was empty for some reason'

c_sensitive_log.debug('Oracle Key loaded')

bucket.temp_dir.cleanup()
