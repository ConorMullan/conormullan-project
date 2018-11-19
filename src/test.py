
import tweepy as tp


tweet = "First Test Tweet"
try:

    if api.update_status(tweet):
        print("Posted")

except tp.TweepError as e:
    print(e)

# public_tweets = api.home_timeline()
#
# for tweet in public_tweets:
#     print(tweet.text)
