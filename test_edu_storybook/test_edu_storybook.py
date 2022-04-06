import unittest

from edu_storybook import app

class test_edu_storybook(unittest.TestCase):
    """
    Tests the main app.py, launch point of the web app.
    """

    def setUp(self):
        self.app = app.test_client

    def test_load(self):
        response = self.app.get('/')
        self.assertEqual(
            response.status_code, 
            200, 
            'HTTP Status code should be okay (200), but was not'
        )
