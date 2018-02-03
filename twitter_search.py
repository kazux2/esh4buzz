from twitter import *
from settings import SETTING

"""
tweepy documet
https://github.com/tweepy/tweepy
"""

"""
Standard search API parameters documentation at 
https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
"""

class TwitterSearch(object):
    CONSUMER_KEY    = SETTING['twitter']['CONSUMER_KEY']
    CONSUMER_SECRET = SETTING['twitter']['CONSUMER_SECRET']
    CALLBACK_URL    = SETTING['twitter']['CALLBACK_URL']

    session = dict()
    oauth_token = ""
    oauth_secret = ""

    twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

    def search(self, search_query, lang = "ja", result_type = "recent"):

        result = self.twitter.search.tweets(q = search_query, lang = lang, result_type = result_type)
        return result

    def session_receiver(self, session):
        self.session = session
        self.oauth_token = session['access_token_key']
        self.oauth_secret = session['access_token_secret']


