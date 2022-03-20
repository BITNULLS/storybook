'''
navbar.py

Makes navbars for all of the other pages.
'''

import jwt
import logging

from core.config import config
from core.sensitive import jwt_key
from core.config import config

from templates import TEMPLATES

log = logging.getLogger('ssg.navbar')
if config['production'] == False:
    log.setLevel(logging.DEBUG)

def make_navbar(authorization: str):
    '''
    Takes in the authorization header from a user.

    :param authorization: The authorization cookie from the user
    '''
    if authorization == None:
        return TEMPLATES['navbar']['logged_out'].substitute()

    token = jwt.decode(authorization.replace('Bearer ', ''), jwt_key, config['jwt_alg'])

    if token['permission'] > 0: # have admin
        return TEMPLATES['navbar']['logged_admin'].substitute()
    else: # do not have admin
        return TEMPLATES['navbar']['logged_user'].substitute()

