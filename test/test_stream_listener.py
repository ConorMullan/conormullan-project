import unittest

from tweepy.api import API
from tweepy.models import Status
from tweepy.streaming import Stream, StreamListener
from src.stream_listener import *
from test.config import create_auth
from mock import MagicMock, patch

class MockReplyToMentionListener(StreamListener)
    def __init__(self, test_case):
        super().__init__()
        self.test_case = test_case
        self.status_count = 0
        self.status_stop_count = 0
        self.connect_cb = None


    def on_error(self, error):
        print("Error: {}".format(error))
        return True

    def on_status(self, status):
        self.status_count += 1
        self.test_case.assertIsInstance(status, Status)
        if self.status_stop_count == self.status_count:
            return False

class TweepyStreamTests(unittest.TestCase):
    def setUp(self):
        self.auth = create_auth()
        self.listener = MockReplyToMentionListener(self)
        self.stream = Stream(self.auth, self.listener, timeout=3.0)

    def tearDown(self):
        self.stream.disconnect()

    def on_status(self):
        API(self.auth).update_status(mock_tweet())

    def test_stream(self):
        self.listener.connect_cb = self.on_connect
        self.listener.status_stop_count = 1
        self.stream.userstream()
        self.assertEqual(self.listener.status_count, 1)

    @skip("Sitestream only available to whitelisted accounts.")
    def test_sitestream(self):
        self.listener.connect_cb = self.on_connect
        self.listener.status_stop_count = 1
        self.stream.sitestream(follow=[self.auth.get_username()])
        self.assertEqual(self.listener.status_count, 1)
