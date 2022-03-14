"""
sensitive.py
    Downloads, loads in, and then deletes all sensitive data files.
    Any error here is critical, and should stop execution of the app.
"""

from .filepath import fix_filepath
from . import bucket
import os
from zipfile import ZipFile
import json
import smtplib
import ssl
from .config import config

# Unzip Wallet
wallet_zip_path = fix_filepath(__file__, 'data/Wallet_EDUStorybook')

if not os.path.isdir(wallet_zip_path):
    os.mkdir(wallet_zip_path)
with ZipFile(bucket.wallet, 'r') as zip_ref:
    zip_ref.extractall(wallet_zip_path)
os.remove(bucket.wallet)

# Get Domain Name
domain_name = None
with open(bucket.domain) as txtfile:
    for line in txtfile.readlines():
        domain_name = str(line)
        break
os.remove(bucket.domain)
assert domain_name is not None and domain_name != '', config['sensitives'][
    'files']['domain_name'] + ' is empty; It should not be empty'

# email login
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
    print("Email Server Error")
    print(e)

# jwt_key Initialization
with open(bucket.jwt) as txtfile:
    for line in txtfile.readlines():
        jwt_key = str(line)
        break
os.remove(bucket.jwt)

# Oracle Key Set up
with open(bucket.oracle_key) as jsonfile:
    oracle_config = json.load(jsonfile)
os.remove(bucket.oracle_key)
assert oracle_config is not None, 'Oracle Key json was empty for some reason'

bucket.temp_dir.cleanup()
