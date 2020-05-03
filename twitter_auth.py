import json
import os

import tweepy

#Twitter APIのアクセストークン
try:
    CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
except KeyError:
    with open('./twitter_keys.json') as f:
        keys_dict = json.load(f)
    CONSUMER_KEY = keys_dict['CONSUMER_KEY']
    CONSUMER_SECRET = keys_dict['CONSUMER_SECRET']
    ACCESS_TOKEN = keys_dict['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = keys_dict['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True)