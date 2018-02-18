# coding: UTF-8
from twitter_search import TwitterSearch

class SearchExecuter(object):


    def execute_twtter_search(self, search_word_dict, search_result):

        twitter_search = TwitterSearch()

        for i in range(len(search_word_dict)):

            if search_word_dict[i] == "":
                continue

            else:
                search_result[i] = twitter_search.search(search_word_dict[i])

        return search_result


    def make_tweet_list_json(self, search_word_dict, search_result, tweet_list_temp, tweet_list_json):

        for i in range(len(search_word_dict)):

            if search_word_dict[i] == "":

                continue

            else:

                for j in range(len(search_result[str(i)]["statuses"])):

                    if search_result[str(i)]["statuses"][j]["text"].startswith("RT "):
                        continue
                    else:
                        tweet_list_temp[j] = ["date", "u_name", "text"]
                        tweet_list_temp[j][0] = search_result[str(i)]["statuses"][j]["created_at"]
                        tweet_list_temp[j][1] = search_result[str(i)]["statuses"][j]["user"]["screen_name"]
                        tweet_list_temp[j][2] = search_result[str(i)]["statuses"][j]["text"]

                        tweet_list_json[str(i)][str(j)] = {"date": tweet_list_temp[j][0],
                                                           "u_name": tweet_list_temp[j][1],
                                                           "text": tweet_list_temp[j][2]}

        return tweet_list_json


    def del_empty_json(self, tweet_list_json, search_word_dict):

        for i in range(len(tweet_list_json)):
            if search_word_dict[i] == "":
                continue

            elif tweet_list_json[str(i)] == {}:
                del tweet_list_json[str(i)]

            else:
                for j in range(len(tweet_list_json[str(i)])):
                    if tweet_list_json[str(i)][str(j)] == "j_init":
                        del tweet_list_json[str(i)][str(j)]

        return tweet_list_json
