import tweepy as tp
from key import *

auth = tp.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tp.API(auth)
print("Test")