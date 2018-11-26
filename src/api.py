import tweepy as tp
from src.auth import Authenticate


auth = Authenticate()
auth = auth.authenticate_app()


api = tp.API(auth)
#tweet = "First"


