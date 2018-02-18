# coding: UTF-8



class JsonFormatter(object):



    def init_tweet_list_json(self, search_word_dict, search_result):

        tweet_list_json = {}

        for i in range(len(search_word_dict)):

            if search_word_dict[i] == "":
                continue

            else:
                tweet_list_json[i] = {}

                for j in range(len(search_result[i]["statuses"])):
                    tweet_list_json[i][j] = "j_init"

        return tweet_list_json



    def input_tweet_list_json(self, search_word_dict, search_result, tweet_list_json):
        tweet_list_temp = {}
        for i in range(len(search_word_dict)):

            if search_word_dict[i] == "":

                continue

            else:

                for j in range(len(search_result[i]["statuses"])):

                    if search_result[i]["statuses"][j]["text"].startswith("RT "):
                        continue
                    else:
                        tweet_list_temp[j] = ["date", "u_name", "text"]
                        tweet_list_temp[j][0] = search_result[i]["statuses"][j]["created_at"]
                        tweet_list_temp[j][1] = search_result[i]["statuses"][j]["user"]["screen_name"]
                        tweet_list_temp[j][2] = search_result[i]["statuses"][j]["text"]

                        tweet_list_json[i][j] = {"date": tweet_list_temp[j][0],
                                                 "u_name": tweet_list_temp[j][1],
                                                 "text": tweet_list_temp[j][2]}

        return tweet_list_json



    def del_empty_json(self, tweet_list_json, search_word_dict):

        for i in range(len(tweet_list_json)):
            if search_word_dict[i] == "":
                continue

            elif tweet_list_json[i] == {}:
                del tweet_list_json[i]

            else:
                for j in range(len(tweet_list_json[i])):
                    if tweet_list_json[i][j] == "j_init":
                        del tweet_list_json[i][j]

        return tweet_list_json



    def search_dict_to_json(self, search_word_dict):
        search_word_json = {}
        for i in range(len(search_word_dict)):
            if search_word_dict[i] == "":
                continue

            else:
                search_word_json[i] = {0: search_word_dict[i]}

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
