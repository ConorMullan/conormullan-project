import tweepy as tp
from src.auth import Auth
tweet = "First"

api = API(Auth())

try:
    if api.update_status(tweet):
        print("Posted")
except tp.TweepError as e:
    print(e)