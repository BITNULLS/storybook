import sys
import os
sys.path.append("edu_storybook/") # Adds higher directory to python modules path.
sys.path.append("edu_storybook/api/") # Adds higher directory to python modules path.
sys.path.append('.')

import unittest
from werkzeug.test import Client

from edu_storybook import app

c = Client(app)

class TestEduStorybook(unittest.TestCase):
    """
    Tests the main app.py, launch point of the web app.
    """

    def test_load(self):
        response = c.get(os.getcwd())
        self.assertEqual(
            response.status_code, 
            200, 
            'HTTP Status code should be okay (200), but was not'
        )
