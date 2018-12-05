import tweepy as tp
from src.forecast import Forecast
from src.authenticate import Authenticate
from datetime import datetime
import schedule
import time


class API:
    def __init__(self):
        self.__auth = Authenticate()
        self.__auth = self.__auth.authenticate_app()
        self.__api = tp.API(self.__auth)

    def update_status(self, text):
        return self.__api.update_status(text)


def task():
    api = API()
    random_forecast = Forecast("None")

    tweet_current_summary = random_forecast.format_current_summary()
    tweet_weekly_summary = random_forecast.format_weekly_summary()

    api.update_status(tweet_weekly_summary)
    api.update_status(tweet_current_summary)
    print("File has executed")
    print("Date and time:", str(datetime.now()))


if __name__ == '__main__':
    # Documentation for schedule found at https://schedule.readthedocs.io/en/stable/
    schedule.every().hour.do(task)
    while True:
        schedule.run_pending()
        time.sleep(2)


