# coding: UTF-8

import json

class Model(object):
    print("have I ever used?")
    def load_search_result(self, path = 'json_data/search_1135_ja.json'):
        f = open(path, 'r')
        search_result_read = json.load(f)
        return search_result_read


    def save_result_tweet(self, path = 'json_data/result_tweet_json.json', tweet_list_json = {}):
        f = open(path, 'w')
        json.dump(tweet_list_json, f, indent=4, ensure_ascii=False)
        print("result_tweet_json saved")

