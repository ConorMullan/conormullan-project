from src.key import keys
from tweepy import OAuthHandler, TweepError


class AuthenticationException(TweepError):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Authenticate:

    def __init__(self):
        self.auth = None
        self.__consumer_key = keys["C_KEY"]
        self.__consumer_secret = keys["C_SECRET"]
        self.__access_token = keys["A_TOKEN"]
        self.__access_token_secret = keys["A_TOKEN_SECRET"]

    # def authenticate_app(self):
    #     try:
    #         self.auth = self.declare_auth()
    #         self.auth = API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
    #         return self.auth
    #     except AuthenticationException as e:
    #         print("Authentication failed, value: {}".format(e))

    def declare_auth(self):
        if self.auth is None:
            try:
                self.auth = OAuthHandler(self.get_consumer_key(),self.get_consumer_secret())
                self.auth.set_access_token(self.get_access_token(), self.get_access_token_secret())
                return self.auth
            except AuthenticationException as e:
                print("Failed to set authentication: {}".format(e.value))
        else:
            return self.auth

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
