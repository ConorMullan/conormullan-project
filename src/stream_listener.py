from tweepy import API
from tweepy.streaming import StreamListener
from tweepy import Stream
from src.authenticate import Authenticate
import json

auth = Authenticate().authenticate_app()
api = API(auth)


# Responds to tweets directed at the bot with "@"
class ReplyToMentionTweet(StreamListener):

    def on_status(self, status):
        if 'RT' not in status.text:
            print('Tweet text: '+status.text)
            s = status.author.screen_name
            print(s)
            try:
                tweet = '@' + s + ' You tweeted with at me!'
                # api.update_status(status=tweet, in_reply_to_status_id=status.id)
            except Exception as e:
                print("Tweet reply failed: {}".format(e))
        return True

    def on_error(self, status):
        # Rate limit
        print("Stream Error: {}".format(str(status)))
        if status == 420:
            return False
        return True # To continue listening


if __name__ == '__main__':
    streamListener = ReplyToMentionTweet()
    twitterStream = Stream(auth, streamListener)
    # Will filter all timeline activities to those that
    # directly pertain to the user. Once connected to the stream,
    # activities are passed on to
    twitterStream.filter(track=['CM46_Project'])
    # twitterStream.filter(follow=1111015900570963969)
