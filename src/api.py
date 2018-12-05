import tweepy as tp
from src.forecast import Forecast
from src.authenticate import Authenticate
# import schedule
# import time


class API:
    def __init__(self):
        self.__auth = Authenticate()
        self.__auth = self.__auth.authenticate_app()
        self.__api = tp.API(self.__auth)

    def update_status(self, text):
        return self.__api.update_status(text)


if __name__ == '__main__':

    api = API()
    random_forecast = Forecast("None")

    tweet_current_summary = random_forecast.format_current_summary()
    tweet_weekly_summary = random_forecast.format_weekly_summary()

    api.update_status(tweet_weekly_summary)
    api.update_status(tweet_current_summary)
