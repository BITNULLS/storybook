'''
user.py

Defines the user model for the `USER_PROFILE` table.
'''

from doctest import debug_script
from typing import Dict
from .exceptions import InvalidDatabaseRowException

class User:
    '''
    A user object, as interpreted from database data.
    '''
    email: str
    first_name: str
    last_name: str
    admin: bool
    school_id: int
    created_on: int
    last_login: int
    password: str
    user_id: str

    def __init__(self, db_row: Dict[str]):
        '''
        Constructor. Initialize this object with a database row.
        '''
        if isinstance(db_row.keys()[0], str):
            self.email = db_row['EMAIL']
            self.first_name = db_row['FIRST_NAME']
            self.last_name = db_row['LAST_NAME']
            self.admin = True if db_row['ADMIN'] == '1' else False
            self.school_id = int(db_row['SCHOOL_ID'])
            self.created_on = int(db_row['CREATED_ON'])
            self.last_login = int(db_row['LAST_LOGIN'])
            self.password = db_row['PASSWORD']
            self.user_id = db_row['USER_ID']
        elif isinstance(db_row.keys()[0], int):
            self.email = db_row[0]
            self.first_name = db_row[1]
            self.last_name = db_row[2]
            self.admin = True if db_row[3] == '1' else False
            self.school_id = int(db_row[4])
            self.created_on = int(db_row[5])
            self.last_login = int(db_row[6])
            self.password = db_row[7]
            self.user_id = db_row[8]
        else:
            raise InvalidDatabaseRowException('The user model was passed a ' + \
                'database row with keys that are neither strings nor ints.')

    def __str__(self):
        return f'User {self.user_id}; {self.last_name}, {self.first_name}'
