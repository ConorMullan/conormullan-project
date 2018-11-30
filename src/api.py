import tweepy as tp
from src.forecast import Forecast
from src.auth import Authenticate
# import schedule
# import time


auth = Authenticate()
auth = auth.authenticate_app()
api = tp.API(auth)


random_forecast = Forecast("None")
tweet = random_forecast.format_current_summary()

api.update_status(tweet)
