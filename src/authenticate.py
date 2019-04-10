from src.key import keys
from tweepy import OAuthHandler


class Authenticate:

    def __init__(self):
        self.__consumer_key = keys["C_KEY"]
        self.__consumer_secret = keys["C_SECRET"]
        self.__access_token = keys["A_TOKEN"]
        self.__access_token_secret = keys["A_TOKEN_SECRET"]

    def authenticate_app(self):
        auth = OAuthHandler(self.get_consumer_key(), self.get_consumer_secret())
        auth.set_access_token(self.get_access_token(), self.get_access_token_secret())
        return auth

    def get_access_token(self):
        if not self.__access_token:
            print("Empty Access Token")
        else:
            return self.__access_token

    def get_access_token_secret(self):
        if not self.__access_token_secret:
            print("Empty Access Token Secret")
        else:
            return self.__access_token_secret

    def get_consumer_key(self):
        if not self.__consumer_key:
            print("Empty Consumer Key")
        else:
            return self.__consumer_key

    def get_consumer_secret(self):
        if not self.__consumer_secret:
            print("Empty Consumer Secret")
        else:
            return self.__consumer_secret
