import unittest
from mock import create_autospec, mock, MagicMock, patch
import unittest
import requests
from src.api import API
import tweepy as tp


class TestApi(unittest.TestCase):

    def setUp(self):
        self.api = API()

    @mock.patch.object(tp.API, 'update_status')
    def test_update_status(self, mock_update_status):
        self.api.update_status("Hello World!")
        mock_update_status.assert_called_with("Hello World!")

    @mock.patch.object(tp.API, 'followers_ids')
    def test_get_my_follower_ids(self, mock_followers_ids):

        print("Mock followers: {}".format(mock_followers_ids))
        followers_ids = self.api.get_my_follower_ids()
        mock_followers_ids.assert_called()
        self.assertEqual(len(followers_ids), len(mock_followers_ids))

    @mock.patch.object(tp.API, 'followers')
    def test_get_my_followers(self, mock_followers):
        followers = self.api.get_my_followers()

        mock_followers.assert_called()
        self.assertEqual(len(followers), len(mock_followers))

