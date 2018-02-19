# coding: UTF-8

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



class TwiSearch(object):

    CONSUMER_KEY    = SETTING['twitter']['CONSUMER_KEY']
    CONSUMER_SECRET = SETTING['twitter']['CONSUMER_SECRET']
    CALLBACK_URL    = SETTING['twitter']['CALLBACK_URL']

    twi = Twitter()

    def __init__(self, sess):
        print("At TwiSearch init")
        print(type(sess))
        print(sess)

        # self.session = sess
        oauth_token = sess['access_token_key']
        oauth_secret = sess['access_token_secret']
        self.twi = Twitter(auth=OAuth(oauth_token, oauth_secret, self.CONSUMER_KEY, self.CONSUMER_SECRET))



    def search(self, search_query, lang = "ja", result_type = "recent"):

        result = self.twi.search.tweets(q = search_query, lang = lang, result_type = result_type)

        return result



    def make_search_result(self, search_word_dict):

        search_result = {}

        for i in range(len(search_word_dict)):

            if search_word_dict[i] == "":
                continue

            else:
                search_result[i] = self.search(search_word_dict[i])

        return search_result


