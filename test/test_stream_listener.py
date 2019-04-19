import unittest
import tweepy as tp
import src.forecast as fc
from tweepy import API
from tweepy.models import Status
from src.authenticate import Authenticate
from src.stream_listener import *
from test.config import create_auth
from mock import mock, patch
from nose.tools import assert_true

TWEET = dict(LARNE='1117215088082128898')


class TweetsTests(unittest.TestCase):
    def setUp(self):
        self.tweet_id = 1117215088082128898
        self.user_id = 1111015900570963969
        self.user_text = "Larne."
        oauth = Authenticate().declare_auth()
        self.my_api = API(auth_handler=oauth)

    # Tweet id: 1117215088082128898
    # Tweet text: @CM46_Project Larne.
    @patch.object(tp.API, 'get_status', return_value=streamApi.get_status('1117215088082128898'))
    def test_two(self, mock_method):
        status = self.my_api.get_status()
        tweets = Tweets(status)
        actual_id = tweets.get_status_id()
        actual_text = tweets.get_user_text().split()[1]
        mock_method.assert_called()
        self.assertEqual(self.tweet_id, actual_id)
        self.assertEqual(self.user_text, actual_text)

    @patch.object(tp.API, 'get_status', return_value=streamApi.get_status('1117215088082128898'))
    def test_search_tweet_for_place(self, mock_get_status):
        status = self.my_api.get_status()
        tweets = Tweets(status)
        tweets.filter_user_tweet_forecast()
        place = tweets.search_tweet_for_place()
        print(place)
        mock_get_status.assert_called()
        self.assertEqual("larne", place)

    @patch.object(tp.API, 'followers_ids', return_value=streamApi.followers_ids(screen_name="CM46_Project"))
    @patch.object(tp.API, 'get_status', return_value=streamApi.get_status('1117215088082128898'))
    def test_is_valid_user(self, mock_get_status, mock_followers_ids):
        status = self.my_api.get_status()
        tweets = Tweets(status)
        result = tweets.is_valid_user()
        mock_get_status.assert_called()
        mock_followers_ids.assert_called()
        assert_true(result)

    @patch.object(tp.API, 'get_status', return_value=streamApi.get_status('1117215088082128898'))
    def test_is_valid_tweet(self, mock_get_status):
        status = self.my_api.get_status()
        tweets = Tweets(status)
        result = tweets.is_valid_tweet()
        mock_get_status.assert_called()
        self.assertTrue(result)

    @patch.object(tp.API, 'get_status', return_value=streamApi.get_status('1117215088082128898'))
    def test_valid_test_error(self, mock_get_status):
        status = self.my_api.get_status()
        tweets = Tweets(status)
        tweets.set_user_text("RT")
        result = tweets.is_valid_tweet()
        mock_get_status.assert_called()
        self.assertFalse(result)

    @patch('src.forecast.Forecast')
    @patch.object(tp.API, 'get_status', return_value=streamApi.get_status('1117215088082128898'))
    def test_str_format_response_tweet(self, mock_get_status, mock_forecast_class):
        status = self.my_api.get_status()
        tweets = Tweets(status)
        tweets.create_tweet()
        larne_forecast = Forecast("larne")
        expected = '@MullanTest {}'.format(larne_forecast.format_weekly_summary())
        result = tweets.str_format_response_tweet()
        self.assertEqual(expected, result)

    @patch.object(tp.API, 'get_status', return_value=streamApi.get_status('1117215088082128898'))
    def test_filter_user_tweet_forecast(self, mock_get_status):
        status = self.my_api.get_status()
        tweets = Tweets(status)
        expected = "cm46project larne"
        result = tweets.filter_user_tweet_forecast()
        mock_get_status.assert_called()
        self.assertEqual(expected, result)

    @patch.object(tp.API, 'get_status', return_value=streamApi.get_status('1117215088082128898'))
    def test_get_user_status(self, mock_get_status):
        expected = self.my_api.get_status()
        tweets = Tweets(expected)
        result = tweets.get_user_status()
        mock_get_status.assert_called()
        self.assertEqual(expected, result)

    @patch.object(tp.API, 'get_status', return_value=streamApi.get_status('1117215088082128898'))
    def test_get_status_id(self, mock_get_status):
        status = self.my_api.get_status()
        tweets = Tweets(status)
        expected = self.tweet_id
        result = tweets.get_status_id()
        mock_get_status.assert_called()
        self.assertEqual(expected, result)

    @patch.object(tp.API, 'get_status', return_value=streamApi.get_status('1117215088082128898'))
    def test_get_user_name(self, mock_get_status):
        status = self.my_api.get_status()
        tweets = Tweets(status)
        expected = "MullanTest"
        result = tweets.get_user_name()
        mock_get_status.assert_called()
        self.assertEqual(expected, result)

    @patch.object(tp.API, 'get_status', return_value=streamApi.get_status('1117215088082128898'))
    def test_get_user_id(self, mock_get_status):
        status = self.my_api.get_status()
        tweets = Tweets(status)
        expected = self.user_id
        result = tweets.get_user_id()
        mock_get_status.assert_called()
        self.assertEqual(expected, result)

    @patch.object(tp.API, 'get_status', return_value=streamApi.get_status('1117215088082128898'))
    def test_get_user_text(self, mock_get_status):
        status = self.my_api.get_status()
        tweets = Tweets(status)
        expected = "@CM46_Project Larne."
        result = tweets.get_user_text()
        mock_get_status.assert_called()
        self.assertEqual(expected, result)

    @patch.object(tp.API, 'get_status', return_value=streamApi.get_status('1117215088082128898'))
    def test_set_user_status(self, mock_get_status):
        status = self.my_api.get_status()
        tweets = Tweets(status)
        expected = tweets.get_user_status()
        tweets.set_user_status(1117215088082128898)
        result = tweets.get_user_status()
        mock_get_status.assert_called()
        self.assertEqual(expected, result)

    @patch.object(tp.API, 'get_status', return_value=streamApi.get_status('1117215088082128898'))
    def test_filter_user_tweet_chatbot(self, mock_get_status):
        status = self.my_api.get_status()
        tweets = Tweets(status)
        expected = "Larne."
        result = tweets.filter_user_tweet_chatbot()
        mock_get_status.assert_called()
        self.assertEqual(expected, result)

    @patch.object(tp.API, 'update_status')
    @patch.object(tp.API, 'get_status', return_value=streamApi.get_status('1117215088082128898'))
    def test_run(self, mock_get_status, mock_update_status):
        status = self.my_api.get_status()
        tweets = Tweets(status)
        tweets.run()
        mock_update_status.assert_called_with(in_reply_to_status_id=tweets.get_status_id(),
                                              status=tweets.create_tweet())
        mock_get_status.assert_called()


if __name__ == "__main__":
    unittest.main()
