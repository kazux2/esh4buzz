# coding: UTF-8

from twitter_search import TwitterSearch
import json



class JsonFormatter(object):

    def search_dict_to_json(self, search_word_dict):
        search_word_json = {}
        for i in range(len(search_word_dict)):
            if search_word_dict[i] == "":
                continue

            else:
                search_word_json[str(i)] = {"0": search_word_dict[i]}

        return search_word_json

    def load_search_result(self, path = 'json_data/search_1135_ja.json'):
        f = open(path, 'r')
        search_result_read = json.load(f)
        return search_result_read


    #  twitter search shouldn't be triggerd here. But needs for tweet_json_init
    def json_init(self, search_word_dict):

        search_result = {}
        tweet_list_temp = {}
        tweet_list_json = {}

        twitter_search = TwitterSearch()

        for i in range(len(search_word_dict)):

            if search_word_dict[i] == "":
                continue

            else:
                search_result[str(i)] = twitter_search.search(search_word_dict[i])

            # tweet_list_json[str(i)] = "i_init"

            if search_word_dict[i] == "":
                continue

            else:
                tweet_list_json[str(i)] = {}

                for j in range(len(search_result[str(i)]["statuses"])):
                    tweet_list_json[str(i)][str(j)] = "j_init"

        return search_result, tweet_list_temp, tweet_list_json



    def tw_json_to_html_json(self, search_word_dict, search_result, tweet_list_temp,tweet_list_json):

        twitter_search = TwitterSearch()

        for i in range(len(search_word_dict)):

            if search_word_dict[i] == "":
                continue

            else:
                search_result[i] = twitter_search.search(search_word_dict[i])


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



    def del_empty_json(self, jsonn, search_word_dict):

        for i in range(len(jsonn)):
            if search_word_dict[i] == "":
                continue

            elif jsonn[str(i)] == {}:
                del jsonn[str(i)]

            else:
                for j in range(len(jsonn[str(i)])):
                    if jsonn[str(i)][str(j)] == "j_init":
                        del jsonn[str(i)][str(j)]

        return jsonn



    def save_result_tweet(self, path = 'json_data/result_tweet_json.json', tweet_list_json = {}):
        f = open(path, 'w')
        json.dump(tweet_list_json, f, indent=4, ensure_ascii=False)
        print("result_tweet_json saved")



    def print_json(self, json, search_word_dict):
        for i in range(len(json)):
            if search_word_dict[i] == "":

                continue

            else:
                for j in range(len(json[str(i)])):
                    print(str(i) +"-"+str(j))
                    print(json[str(i)][str(j)]["date"])
                    print(json[str(i)][str(j)]["u_name"])
                    print(json[str(i)][str(j)]["text"])
                    print("")



