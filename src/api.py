
from tweepy import Stream

import tweepy as tp
import time
from src.forecast import Forecast
from src.authenticate import Authenticate
from src.stream_listener import ReplyToMentionListener
# import schedule
# import time
# self.__auth = self.__auth.authenticate_app()
# self.__api = tp.API(self.__auth)
# self.__api = self.__auth


class API(object):

    def __init__(self):
        try:
            self.auth = Authenticate().declare_auth()
            self.api = tp.API(auth_handler=self.auth, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True, compression=True)
            print(str(self.api.rate_limit_status))
        except tp.TweepError as e:
            print("API error: {}".format(e.response))

    def update_status(self, text):
        return self.api.update_status(text)

    def get_my_followers(self):
        followers = self.api.followers(self.api.me())
        return followers

    def get_my_follower_ids(self):
        follower_ids = self.api.followers_ids(self.api.me())
        return follower_ids


if __name__ == '__main__':

    # random_forecast = Forecast("None")
    # user_forecast = Forecast("dungiven")
    # print(user_forecast.format_weekly_summary())
    # print(user_forecast.get_alert())
    # tweet_current_summary = random_forecast.format_current_summary()
    # tweet_weekly_summary = random_forecast.format_weekly_summary()
    api = API()
    print(api.get_my_follower_ids())
    # api.update_status(tweet_weekly_summary)
    # api.update_status(tweet_current_summary)
    # print(api.get_followers())
    # ids = api.get_my_follower_ids()
    # print(ids)
    # ids = []

    # myStreamListener = ReplyToMentionListener()
    # myStream = Stream(auth=Authenticate.declare_auth, listener=myStreamListener)
    # myStream.filter(track=['CM46_Project'])
