"""
helper.py
    Helper functions not distinctly part of auth, bucket, db, or other "parts"
    of our app.

Functions:
    allowed_file(...)
    label_results_from(...)
    send_email(...)
"""

from turtle import st
import cx_Oracle
import smtplib
from . import sensitive as sensitive
import os
import logging
from core.reg_exps import re_redirect_link

ALLOWED_EXTENSIONS = {'pdf', 'ppt', 'pptx'}

def allowed_file(filename):
    """
    checks that a file extension is one of the allowed extensions, defined by ALLOWED_EXTENSIONS

    :param filename: name of file to be uploaded
    :returns: bool. True if file extension allowed, False if extension not allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def fix_filepath(filepath: str, file: str) -> str:
    """
    When referencing a file from a Python file that is not the original start of
    the Python program, a filepath must be corrected from the current file's
    __file__ path, as to start using the current Python file as a based for
    relative file referencing.

    Example:
        a.py
        module_b/
            __init__.py
            c.py
            config.txt
        
        If a.py imports module_b.c, and if c.py imports c.config as 
        "./config.txt", it will fail since the Python interpreter pathing is
        relative to the start script, a.py.
    
    You would call this function as
        fix_filepath(__file__, 'relative/file/path.txt')
    
    :param filepath: The current file context, __file__.
    :param file: Relative file to reference.
    """
    return os.path.join(os.path.dirname(os.path.abspath(filepath)), file)


def label_results_from(cursor: cx_Oracle.Cursor):
    """
    Labels results from a cursor into a dictionary where like
    {
        "column1": "value1",
        "col2":    "val2",
        ...
    }
    I am amazed that cx_Oracle does not provide this. Labeling the columns in 
    the returned data is so basic. Why doesn't it do it. I checked the docs.
    Oracle thinks this is reasonable. I do not think this is reasonable, but 
    okay.

    :param cursor: A cursor that has been .execute[d].
    :type cursor: cx_Oracle.Cursor

    :returns: The same cursor with the row factory applied.
    """
    columns = [col[0] for col in cursor.description]
    cursor.rowfactory = lambda *args: dict(zip(columns, args))
    return cursor
    
def sanatize_redirects(redirect_link: str) -> str:
    """
    Determines if a given redirect link is a valid relative or absolute path

    :param redirect_link: The link to validate

    :returns: The relative or absolute path if it is valid, '/' if it is not.
    """
    if re_redirect_link.match(redirect_link):
        logging.warning("Redirect Link is not a valid relative or absolute path.")
        return '/'
    else:
        return redirect_link