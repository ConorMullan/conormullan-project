
import tweepy as tp
from .config import *
import unittest
import random


class TestAuthentication(unittest.TestCase):

    def test_authentication_app(self):
        # self.auth = self.auth.authenticate_app()
        # api = tp.API(self.auth)
        #
        # auth_2 = tp.OAuthHandler(self.consumer_key, self.consumer_secret)
        # auth_2.set_access_token(self.access_token, self.token_secret)
        # api_2 = tp.API(auth_2)
        #
        # self.assertIs(api, api_2)
        auth = tp.OAuthHandler(consumer_key, consumer_secret)

        auth_url = auth.get_authorization_url()
        print("Please authorize: "+auth_url)
        verifier = input('PIN: ').strip()
        self.assertTrue(len(verifier) > 0)
        input_access_token = auth.get_access_token(verifier)
        self.assertTrue(input_access_token is not None)

    def test_get_access_token(self):
        self.assertEqual(self.access_token, self.auth.get_access_token())

    def test_get_access_token_secret(self):
        self.assertEqual(self.token_secret, self.auth.get_access_token_secret())

    def test_get_consumer_key(self):
        self.assertEqual(self.consumer_key, self.auth.get_consumer_key())

    def test_get_consumer_secret(self):
        self.assertEqual(self.consumer_secret, self.auth.get_consumer_secret())


if __name__ == '__main__':
    unittest.main()
