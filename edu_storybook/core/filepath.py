"""
filepath.py
    Fix for Python's inane doubly relative file pathing.
    So, I give up. Here it is on its own.
"""

import os

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

