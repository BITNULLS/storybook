'''
book.py

Defines the book model for the `BOOK` table.
'''

from doctest import debug_script
from typing import Dict
from .exceptions import InvalidDatabaseRowException

class Book:
    '''
    A `book` object, as interpreted from database data.
    '''
    book_id: int
    book_name: str
    created_on: int
    url: str
    description: str
    page_count: int
    folder: str

    def __init__(self, db_row: Dict[str]):
        '''
        Constructor. Initialize this object with a database row.
        '''
        if isinstance(db_row.keys()[0], str):
            self.book_id = int(db_row['BOOK_ID'])
            self.book_name = db_row['BOOK_NAME']
            self.created_on = int(db_row['CREATED_ON'])
            self.url = db_row['URL']
            self.description = db_row['DESCRIPTION']
            self.page_count = int(db_row['PAGE_COUNT'])
            self.folder = db_row['FOLDER']
        elif isinstance(db_row.keys()[0], int):
            self.book_id = int(db_row[0])
            self.book_name = db_row[1]
            self.created_on = int(db_row[2])
            self.url = db_row[3]
            self.description = db_row[4]
            self.page_count = int(db_row[5])
            self.folder = db_row[6]
        else:
            raise InvalidDatabaseRowException('The book model was passed a ' + \
                'database row with keys that are neither strings nor ints.')

    def __str__(self):
        return f'Book {self.book_id}, {self.book_name}, with {self.page_count} pages'
