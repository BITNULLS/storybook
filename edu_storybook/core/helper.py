"""
helper.py

Helper functions not distinctly part of auth, bucket, db, or other "parts" of
our app.
"""

import cx_Oracle
import smtplib
from edu_storybook.core import sensitive as sensitive
import os
import logging
from edu_storybook.core.reg_exps import re_redirect_link
from edu_storybook.core.config import Config

ALLOWED_EXTENSIONS = {'pdf', 'ppt', 'pptx'}

c_helper_log = logging.getLogger('core.helper')
if Config.production == False:
    c_helper_log.setLevel(logging.DEBUG)


def allowed_file(filename) -> bool:
    """
    checks that a file extension is one of the allowed extensions, defined by ALLOWED_EXTENSIONS

    :param filename: name of file to be uploaded
    :returns: bool. True if file extension allowed, False if extension not allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def label_results_from(cursor: cx_Oracle.Cursor):
    """
    Labels results from a cursor into a dictionary where like:
    ```
    {
        "column1": "value1",
        "col2":    "val2",
        ...
    }
    ```
    I am amazed that cx_Oracle does not provide this. Labeling the columns in
    the returned data is so basic. Why doesn't it do it. I checked the docs.
    Oracle thinks this is reasonable. I do not think this is reasonable, but
    okay.

    Args:
     - cursor: A cursor that has been .execute[d].

    Returns: The same cursor with the row factory applied.
    """
    columns = [col[0] for col in cursor.description]
    cursor.rowfactory = lambda *args: dict(zip(columns, args))
    return cursor


def sanitize_redirects(redirect_link: str) -> str:
    """
    Determines if a given redirect link is a valid relative or absolute path.

    Args:
     - redirect_link: The link to validate

    Returns: The relative or absolute path if it is valid, `'/'` if it is not.
    """
    if re_redirect_link.match(redirect_link) is None:
        c_helper_log.warning(f"Redirect Link '{redirect_link}' is not a valid relative or absolute path.")
        return '/'
    else:
        return redirect_link


def has_no_empty_params(rule: dict) -> bool:
    '''
    Checks if a Flask rule has no arguments.

    Args:
     - rule: A Flask rule cast into a dictionary.

    Returns: True if the rule has no params, False if not.
    '''
    defaults = rule['defaults'] if rule['defaults'] is not None else ()
    arguments = rule['arguments'] if rule['arguments'] is not None else ()
    return len(defaults) >= len(arguments)
