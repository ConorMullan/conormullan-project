import unittest
import tweepy as tp
from tweepy import API
from tweepy.models import Status
from src.authenticate import Authenticate
from src.stream_listener import *
from test.config import create_auth
from mock import MagicMock, mock, patch
from nose.tools import assert_true

TWEET = dict(LARNE='1117215088082128898')


class MockReplyToMentionListener(StreamListener):
    def __init__(self, test_case):
        super().__init__()
        self.test_case = test_case
        self.status_count = 0
        self.status_stop_count = 0
        self.connect_cb = None

    def on_connect(self):
        if self.connect_cb:
            self.connect_cb()

    def on_timeout(self):
        self.test_case.fail('timeout')
        return False

    def on_error(self, error):
        print("Error: {}".format(error))
        return True

    @mock.patch.object(tp.API, 'update_status')
    def on_status(self, status):
        self.status_count += 1
        self.test_case.assertIsInstance(status, Status)
        if self.status_stop_count == self.status_count:
            return False


# @patch.object(tp.API, 'get_status')
class TweetsTests(unittest.TestCase):
    def setUp(self):
        self.mock_tweet = "Hello!"
        oauth = Authenticate().declare_auth()
        self.api = API(auth_handler=oauth)
        self.tweets = Tweets


        # self.listener = MockReplyToMentionListener(self)
        # self.stream = Stream(self.api.auth, self.listener, timeout=3.0)
        # tweets = Tweets()
        # self.tweet = "Hello, I would like weather for belfast"
        # self.listener = MockReplyToMentionListener(self)
        # self.stream = Stream(self.auth, self.listener, timeout=3.0)

    # Tweet id: 1117215088082128898
    # Tweet text: @CM46_Project Larne.
    @mock.patch.object(tp.API, 'get_status', return_value=myApi.get_status('1117215088082128898'))
    def test_two(self, mock_method):
        tweet_id = 1117215088082128898
        tweet_text = "Larne."
        get_tweet = self.api.get_status(1117215088082128898)
        actual_id = get_tweet.id
        actual_text = get_tweet.text.split()[1]
        self.assertEqual(actual_id, tweet_id)
        self.assertEqual(actual_text, tweet_text)

    # def test_search_tweet_for_place(self):
    #     place = search_tweet_for_place(self.tweet)
    #     place = str(place)
    #     self.assertEqual(place, "belfast")

    # def test_valid_user(self):

    # def filter_user_tweet(self):
    #     tweet_lower = self.get_user_text()
    #     self.filtered_tweet = tweet_lower.translate(str.maketrans('', '', string.punctuation))
    #     return self.filtered_tweet

    # def test_filter_user_tweet(self):
    #     expected = "Hello"
    #     actual = self.tweets.filter_user_tweet()
    #     self.assertEqual(actual, expected)

    # def tearDown(self):
    #     self.stream.disconnect()
    #
    # def on_status(self):
    #     API(self.auth).update_status(mock_tweet())
    #
    def test_stream(self):
        self.listener.connect_cb = self.on_connect
        self.listener.status_stop_count = 1
        self.stream.filter(track="Hello")
        self.assertEqual(self.listener.status_count, 1)
    #
    # @skip("Sitestream only available to whitelisted accounts.")
    # def test_sitestream(self):
    #     self.listener.connect_cb = self.on_connect
    #     self.listener.status_stop_count = 1
    #     self.stream.sitestream(follow=[self.auth.get_username()])
    #     self.assertEqual(self.listener.status_count, 1)


if __name__ == "__main__":
    unittest.main()
