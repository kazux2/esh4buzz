# coding: UTF-8

from twitter_search import TwitterSearch
import json



class JsonFormatter(object):

    def input_tweet_list_json(self, search_word_dict, search_result, tweet_list_temp, tweet_list_json):

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



    def search_dict_to_json(self, search_word_dict):
        search_word_json = {}
        for i in range(len(search_word_dict)):
            if search_word_dict[i] == "":
                continue

            else:
                search_word_json[str(i)] = {"0": search_word_dict[i]}

        return search_word_json
    #
    #
    # def print_json(self, json, search_word_dict):
    #     for i in range(len(json)):
    #         if search_word_dict[i] == "":
    #
    #             continue
    #
    #         else:
    #             for j in range(len(json[str(i)])):
    #                 print(str(i) +"-"+str(j))
    #                 print(json[str(i)][str(j)]["date"])
    #                 print(json[str(i)][str(j)]["u_name"])
    #                 print(json[str(i)][str(j)]["text"])
    #                 print("")
