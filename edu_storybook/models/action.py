'''
action.py

Defines the action model for the `ACTION` table.
'''

from doctest import debug_script
from typing import Dict
from .exceptions import InvalidDatabaseRowException

class Action:
    '''
    An action object, as interpreted from database data.
    '''
    user_id: str
    action_start: int
    action_stop: int
    book_id: int
    detail_id: int

    def __init__(self, db_row: Dict[str]):
        '''
        Constructor. Initialize this object with a database row.
        '''
        if isinstance(db_row.keys()[0], str):
            self.user_id = db_row['USER_ID']
            self.action_start = int(db_row['ACTION_START'])
            self.action_stop = int(db_row['ACTION_STOP'])
            self.book_id = int(db_row['BOOK_ID'])
            self.detail_id = int(db_row['DETAIL_ID'])
        elif isinstance(db_row.keys()[0], int):
            self.user_id = db_row[0]
            self.action_start = int(db_row[1])
            self.action_stop = int(db_row[2])
            self.book_id = int(db_row[3])
            self.detail_id = int(db_row[4])
        else:
            raise InvalidDatabaseRowException('The action model was passed a ' + \
                'database row with keys that are neither strings nor ints.')

    def __str__(self):
        return f'Action started on {self.action_start} to {self.action_stop} on Book {self.book_id}'
