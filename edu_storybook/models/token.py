'''
token.py

Defines the token model for the JWT token that is stored in the user's 
`Authorization` cookie.
'''

from doctest import debug_script
from typing import Dict
from .exceptions import InvalidDatabaseRowException

class Token:
    '''
    A JWT token object, as interpreted from the user.
    '''

    iat: int
    '''
    Issued At Time (IAT), when a token was issued, epoch time as an integer.
    '''

    session: str
    '''
    Unique ID of session, UUID4.
    '''

    sub: str
    '''
    The ID of a user, unique, 32 characters.
    '''

    permission: int
    '''
    The permission level of a user.

    Meanings:
     - 0 means a regular user.
     - 1 means an administrator.
    '''

    def __init__(self, token: Dict[str]):
        '''
        Constructor. Initialize this object with a database row.
        '''
        self.iat = token['iat']
        self.session = token['session']
        self.sub = token['sub']
        self.permission = token['permission']

    def __str__(self):
        return f'Token issued at {self.iat}, for user {self.sub}, permission {self.permission}'