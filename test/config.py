import unittest
from src.key import keys

from tweepy.auth import OAuthHandler
from tweepy.api import API

consumer_key = keys["C_KEY"]
consumer_secret = keys["C_SECRET"]
access_token = keys["A_TOKEN"]
access_token_secret = keys["A_TOKEN_SECRET"]


class TweepyTestCase(unittest.TestCase):
    def setUp(self):
        self.auth = create_auth()
        self.api = API(self.auth)


def create_auth():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth



