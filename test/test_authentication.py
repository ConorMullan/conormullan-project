
from src.authenticate import Authenticate
from .config import *
import unittest
from src.key import keys
from tweepy import OAuthHandler


class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.auth = Authenticate()

    def test_declare_auth(self):
        expected = OAuthHandler(keys["C_KEY"], keys["C_SECRET"])
        expected.set_access_token(keys["A_TOKEN"], keys["A_TOKEN_SECRET"])

        result = self.auth.declare_auth()
        self.assertIs(type(expected), type(result))

    def test_get_access_token(self):
        self.assertEqual(keys["A_TOKEN"], self.auth.get_access_token())

    def test_get_access_token_secret(self):
        self.assertEqual(keys["A_TOKEN_SECRET"], self.auth.get_access_token_secret())

    def test_get_consumer_key(self):
        self.assertEqual(keys["C_KEY"], self.auth.get_consumer_key())

    def test_get_consumer_secret(self):
        self.assertEqual(keys["C_SECRET"], self.auth.get_consumer_secret())


if __name__ == '__main__':
    unittest.main()
