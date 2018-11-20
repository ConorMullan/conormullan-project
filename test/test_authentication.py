import unittest
from src.key import *
from src.auth import Auth


class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.consumer_key = C_KEY
        self.consumer_secret = C_SECRET
        self.access_token = A_TOKEN
        self.token_secret = A_TOKEN_SECRET

    def test_authentication(self):
        self.auth = Auth()
        return self.auth.authenticate_app()

    def test_get_access_token(self):
        self.auth = Auth()
        self.assertEqual(self.access_token, self.auth.get_access_token())

    def test_get_access_token_secret(self):
        self.auth = Auth()
        self.assertEqual(self.token_secret, self.auth.get_access_token_secret())

    def test_get_consumer_key(self):
        self.auth = Auth()
        self.assertEqual(self.consumer_key, self.auth.get_consumer_key())

    def test_get_consumer_secret(self):
        self.auth = Auth()
        self.assertEqual(self.consumer_secret, self.auth.get_consumer_secret())


if __name__ == '__main__':
    unittest.main()
