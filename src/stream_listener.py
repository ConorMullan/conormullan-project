import string
from tweepy import API
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import TweepError
from time import sleep
from src.authenticate import Authenticate
from data.places import places
from src.forecast import Forecast

# from nmt_chatbot.inference import inference

auth = Authenticate().declare_auth()
myApi = API(auth)


# Exceptions
class TweetTooLong(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NoResponse(TweepError):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# Responds to tweets directed at the bot with "@"
class ReplyToMentionListener(StreamListener):

    def on_status(self, status):

        response = create_tweet(status)
        print('Tweet text: ' + status.text, '\n')
        print(response)
        try:
            myApi.update_status(status=response, in_reply_to_status_id=status.id)
            sleep(10)
        except NoResponse as e:
            print("Tweet reply failed: {}".format(e))

        return True

    def on_error(self, status):
        # Rate limit
        print("Stream Error: {}".format(str(status)))
        if status == 420:
            return False
        return True  # To continue listening


def valid_tweet(status):
    if valid_user(status.author.id):
        if 'RT' not in status.text:
            return True


# Checks if user is a follower i.e. followers can tweet
def valid_user(user_id):
    followers_ids = myApi.followers_ids(screen_name="CM46_Project")
    print(followers_ids)
    print(user_id)
    if user_id in followers_ids:
        return True


def search_tweet_for_place(tweet):
    for word in tweet.split():
        if word in places.keys():
            user_place = word
            return user_place


# Might use this or just stop the code instead
# def response_invalid_user():
#     return print("Please follow the account to whitelist you")
# Creates the text and format for the tweet response
def create_tweet(status):
    if valid_tweet(status):
        text = ""
        tweet_lower = status.text.lower()
        filtered_tweet = tweet_lower.translate(str.maketrans('', '', string.punctuation))
        print(filtered_tweet)
        if any(s in filtered_tweet for s in places.keys()):
            place = search_tweet_for_place(filtered_tweet)
            user_forecast = Forecast("{}".format(place))
            text += user_forecast.format_weekly_summary()
        else:
            text = "Placeholder"
    else:
        text = "Please follow the account to white list you"
    print(text)
    response = '@{} {}'.format(status.author.screen_name, text)
    if len(response) > 240:
        raise TweetTooLong("Response cannot have more than 240 characters. The number of characters was: {}".format(
            len(response)))
    return response


if __name__ == '__main__':
    # Will filter all timeline activities to those that
    # directly pertain to the user. Once connected to the stream,
    # activities are passed on to
    myStreamListener = ReplyToMentionListener()
    myStream = Stream(auth=myApi.auth, listener=myStreamListener)
    # CM46_Project
    myStream.filter(track=['CM46_Project'])

