'''
answer.py

Defines the answer model for the `ANSWER` table.
'''

from doctest import debug_script
from typing import Dict
from .exceptions import InvalidDatabaseRowException

class Answer:
    '''
    An action object, as interpreted from database data.
    '''
    answer_id: str
    question_id: int
    answer: str
    correct: int

    def __init__(self, db_row: Dict[str]):
        '''
        Constructor. Initialize this object with a database row.
        '''
        if isinstance(db_row.keys()[0], str):
            self.answer_id = int(db_row['ANSWER_ID'])
            self.question_id = int(db_row['QUESTION_ID'])
            self.answer = db_row['ANSWER']
            self.correct = True if db_row['CORRECT'] == '1' else False
        elif isinstance(db_row.keys()[0], int):
            self.answer_id = int(db_row[0])
            self.question_id = int(db_row[1])
            self.answer = db_row[2]
            self.correct = True if db_row[3] == '1' else False
        else:
            raise InvalidDatabaseRowException('The action model was passed a ' + \
                'database row with keys that are neither strings nor ints.')

    def __str__(self):
        return f'Action started on {self.action_start} to {self.action_stop} on Book {self.book_id}'
