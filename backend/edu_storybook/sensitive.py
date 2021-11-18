import bucket
import os
from zipfile import ZipFile
import json
import smtplib
import ssl

with open('data/config.json') as jsonfile:
    config = json.load(jsonfile)
assert config is not None, 'Could not find data/config.json file.'
# TODO: Relocate in future when every part of server.py is in the module

wallet = bucket.download_bucket_file("Wallet_EDUStorybook.zip", '../data')
domain = bucket.download_bucket_file("domain.txt", '../data')
email = bucket.download_bucket_file("email.password", '../data')
jwt = bucket.download_bucket_file("jwt.key", '../data')
oracle_key = bucket.download_bucket_file("oracle_key.json", '../data')

# Unzip Wallet
if not os.path.isdir("../data/Wallet_EDUStorybook"):
    os.mkdir("../data/Wallet_EDUStorybook")
with ZipFile(wallet, 'r') as zip_ref:
    zip_ref.extractall("../data/Wallet_EDUStorybook")
os.remove(wallet)

# Get Domain Name
domain_name = None
with open(domain) as txtfile:
    for line in txtfile.readlines():
        domain_name = str(line)
        break
os.remove(domain)
assert domain_name is not None and domain_name != '', config['sensitives'][
    'files']['domain_name'] + ' is empty; It should not be empty'


# email login
with open(email) as email_config:
    email_login = json.load(email_config)
    email_password = email_login['password']
os.remove(email)

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
with open(jwt) as txtfile:
    for line in txtfile.readlines():
        jwt_key = str(line)
        break
os.remove(jwt)

# Oracle Key Set up
with open(oracle_key) as jsonfile:
    oracle_config = json.load(jsonfile)
os.remove(oracle_key)
assert oracle_config is not None, 'Oracle Key json was empty for some reason'
