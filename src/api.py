import tweepy as tp
from src.auth import Authenticate


auth = Authenticate()
auth = auth.authenticate_app()

# auth = OAuthHandler(self.get_consumer_key(), self.get_consumer_secret())
# auth.set_access_token(self.get_access_token(), self.get_access_token_secret())

api = tp.API(auth)
#tweet = "First"

#try
public_tweets = api.home_timeline()
#except tp.TweepError as e:
    #print(e)

for tweet in public_tweets:
    print(tweet.text)

# try:
#     if api.update_status(tweet):
#         print("Posted")
# except tp.TweepError as e:
#     print(e)