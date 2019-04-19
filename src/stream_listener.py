import string
import logging
from nmt_chatbot._deployment.inference import inference
from tweepy import API
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import TweepError
from time import sleep
from src.authenticate import Authenticate
from data.places import places
from src.forecast import Forecast


auth = Authenticate().declare_auth()
streamApi = API(auth)


# Exceptions
class TweetTooLong(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NoPlaceFound(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BotNoResponse(TweepError):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# Responds to tweets directed at the bot with "@"
class ReplyToMentionListener(StreamListener):

    def on_status(self, status):
        try:
            tweets = Tweets(status)
            tweets.run()
            # streamApi.update_status(status=response, in_reply_to_status_id=status.id)
            sleep(10)
        except BotNoResponse as e:
            print("Tweet reply failed: {}".format(e))
        print("Tweet id: {}".format(Tweets(status).get_status_id()))
        print('Tweet text: ' + status.text, '\n')
        return True

    # When StreamListener receives an error, this receives and presents the error,
    # Continues on if it is not affecting rate limit
    def on_error(self, status):
        # Rate limit
        print("Stream Error: {}".format(str(status)))
        if status == 420:
            return False
        return True  # To continue listening


# Class for handling users tweets and creating tweets
class Tweets:
    def __init__(self, status):
        self.user_status = status
        self.tweet_id = status.id
        self.filtered_tweet = ""
        # My response text to the sent status
        self.response_text = ""

    # Returns the status sent to me
    def get_user_status(self):
        return self.user_status

    # Returns the status sent to me id
    def get_status_id(self):
        return self.tweet_id

    # Returns the authors screen name of the status sent to me
    def get_user_name(self):
        return self.user_status.author.screen_name

    # Returns the user id of the status sent to me author
    def get_user_id(self):
        return self.user_status.author.id

    # Returns the text within the status sent to me
    def get_user_text(self):
        return self.user_status.text

    def set_user_text(self, text):
        self.user_status.text = text

    # Mostly for testing to create a status instead of calling Stream
    def set_user_status(self, tweet_id):
        self.user_status = streamApi.get_status(tweet_id)

    # Checks if tweet and user is
    def is_valid_tweet(self):
        if self.is_valid_user():
            if 'RT' not in self.get_user_text():
                return True

    # Checks if user is in the followers list, which is being used as a whitelist
    def is_valid_user(self):
        user_id = self.get_user_id()
        followers_ids = streamApi.followers_ids(screen_name="CM46_Project")
        print(followers_ids)
        print(user_id)
        if user_id in followers_ids:
            return True

    # Searches the tweet for a place to query within a dictionary
    def search_tweet_for_place(self):
        tweet = self.filtered_tweet
        print(tweet)
        if tweet is None:
            tweet = self.filter_user_tweet_forecast()
        for word in tweet.split():
            if word in places.keys():
                user_place = word
                print(user_place)
                return user_place

    # Filters the tweet to search for a forecast
    def filter_user_tweet_forecast(self):
        tweet_lower = self.get_user_text().lower()
        self.filtered_tweet = tweet_lower.translate(str.maketrans('', '', string.punctuation))
        return self.filtered_tweet

    # Filters the tweet to remove the mention for input data for the chatbot
    def filter_user_tweet_chatbot(self):
        tweet = self.get_user_text()
        inference_input = tweet.split(" ", 1)[1]
        return inference_input

    def str_format_response_tweet(self):
        return '@{} {}'.format(self.get_user_name(), self.response_text)

    # Does a whole lot, probably too much:
    # - Checks if user wants a forecast or chatbot response
    # - Formats the user status for validation
    # - Formats the response text
    # - Returns response
    # - Finally, raises if response is too long
    def create_tweet(self):
        if self.is_valid_tweet():
            filtered_tweet = self.filter_user_tweet_forecast()
            print("Filtered tweet: {}".format(filtered_tweet))

            if any(s in filtered_tweet for s in places.keys()):
                place = self.search_tweet_for_place()
                print(place)
                user_forecast = Forecast("{}".format(place))
                self.response_text = user_forecast.format_weekly_summary()

            else:
                inference_input = self.filter_user_tweet_chatbot()
                inference_dict = inference("{}".format(inference_input))
                answers = inference_dict["answers"]
                print("\n Answers: {} \n".format(answers))
                best_index = inference_dict.get("best_index")
                print("Best index: {} \n".format(best_index))
                # Negative index represents poor results
                if best_index == -1:
                    self.response_text = answers[1]
                else:
                    best_answer = answers[best_index]
                    self.response_text = best_answer
                    print("Best answer: {} \n".format(best_answer))
                # Sometimes a empty result will enter, this won't be accepted
                if not self.response_text:
                    self.response_text = answers[2]
                print(inference)
                print("Chatbot response: {}".format(self.response_text))
        else:
            self.response_text = "Please follow the account to white list you and make sure tweet doesn't contain RT." \
                                 " Thank you"

        response = self.str_format_response_tweet()
        if len(response) > 240:
            raise TweetTooLong("Response cannot have more than 240 characters. The number of characters was: {}".format(
                len(response)))
        return response

    # Calls create_tweet method and inputs it as parameter for update_status
    def run(self):
        response = self.create_tweet()
        print(response)
        streamApi.update_status(status=response, in_reply_to_status_id=self.get_status_id())


# if __name__ == '__main__':
#     # Will filter all timeline activities to those that
#     # directly pertain to the user. Once connected to the stream,
#     # activities are passed on to
#     try:
#         myStreamListener = ReplyToMentionListener()
#         myStream = Stream(auth=streamApi.auth, listener=myStreamListener)
#     # CM46_Project
#         myStream.filter(track=['CM46_Project'])
#     except TweepError as e:
#         logging.exception(e)
