import logging
from tweepy import Stream, TweepError
import tweepy as tp
from src.forecast import Forecast
from src.authenticate import Authenticate
from src.stream_listener import ReplyToMentionListener
import schedule
import random
import time


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

    def get_api(self):
        return self.api

    def get_auth(self):
        return self.api.auth


def job():
    random_forecast = Forecast("None")
    summaries = [random_forecast.format_current_summary(), random_forecast.format_weekly_summary()]
    rnd = random.randint(0, 1)
    summary = summaries[rnd]
    print(summary)
    home_api = API()
    home_api.update_status(summary)


def stream_job():
    try:
        my_stream_listener = ReplyToMentionListener()
        my_stream = Stream(auth=API().get_auth(), listener=my_stream_listener)
    # CM46_Project
        my_stream.filter(track=['CM46_Project'])
    except TweepError as e:
        logging.exception(e)


if __name__ == '__main__':
    job()
    stream_job()

    schedule.every().hour.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)



