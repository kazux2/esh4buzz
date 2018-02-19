# coding: UTF-8

import logging
from flask import Flask, redirect, render_template, request, url_for, session
import tweepy
from settings import SETTING
from timer import Timer


CONSUMER_KEY    = SETTING['twitter']['CONSUMER_KEY']
CONSUMER_SECRET = SETTING['twitter']['CONSUMER_SECRET']
CALLBACK_URL    = SETTING['twitter']['CALLBACK_URL']

sess = {}

app = Flask(__name__)
app.secret_key = SETTING['flask']['SECRET_KEY']

timer = Timer()


"""
/
    top page
/detail
    service detail
/oauth
    twitter oauth for request token
/oauth/verify
    oauth info reciever (will not show on client)
/search
    search console
/result
    result
"""



@app.route("/")
def top():
    return render_template("top.html")



@app.route("/detail")
def detail():
    return render_template("detail.html")



@app.route('/oauth', methods=['GET'])
def oauth():
    # for desk top app, giving callback_url causes an error
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    try:
        redirect_url = auth.get_authorization_url()
        # sess['request_token'] = (auth.request_token)
        session['request_token'] = (auth.request_token)
        print("debug ---1---")
        print(session)
        return redirect(redirect_url)

    except tweepy.TweepError:
        print('Error! Failed to get request token')



@app.route("/verify")
def verify():

    verifier = request.args['oauth_verifier']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    print("debug ---2---")
    print(session)
    auth.request_token = {'oauth_token': session['request_token']['oauth_token'],
                          'oauth_token_secret': session['request_token']['oauth_token_secret']}

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')

    api = tweepy.API(auth)

    session['api'] = api
    session['access_token_key'] = auth.access_token
    session['access_token_secret'] = auth.access_token_secret

    return redirect(url_for('search'))



@app.route("/search")
def search():
    return render_template("search.html")



@app.route("/result", methods=['post'])
def result():
    if request.method == 'POST':

        timer.start()

        query = request.form["target_text"]

        from text_segmentation import TextSegmentation
        txt_seg = TextSegmentation()
        r_dict           = txt_seg.segment_text(query, 99)       # query, limit
        r_dict           = txt_seg.join_dict_elements(r_dict, 3) # minimum elements
        search_word_dict = txt_seg.reindex_r_dict(r_dict)
        #debug
        # print("1 r_dict")
        # print(r_dict)
        # print("----------------------")
        print("----- TextSegmentation ----- Duration  : {}".format(timer.stop()))


        timer.start()
        print("At router /request")
        print(type(session))
        print(session)
        from twi_search import TwiSearch
        twi = TwiSearch(session)
        search_result = twi.make_search_result(search_word_dict)

        print("----- TwiSearch        ----- Duration  : {}".format(timer.stop()))


        timer.start()

        from json_formatter import JsonFormatter
        jf = JsonFormatter()
        init_tweet_list_json = jf.init_tweet_list_json(search_word_dict, search_result)
        search_word_json = jf.search_dict_to_json(search_word_dict)
        tweet_list_json = jf.input_tweet_list_json(search_word_dict, search_result, init_tweet_list_json)
        tweet_list_json = jf.del_empty_json(tweet_list_json, search_word_dict)

        print("----- JsonFormatter    ----- Duration  : {}".format(timer.stop()))

        # Save function
        # from model import Model
        # model = Model()
        # model.save_result_tweet('json_data/result_tweet_json8.json', tweet_list_json)
        # tweet_list_json = model.load_search_result('json_data/result_tweet_json8.json')

        return render_template("result.html", tweet_list_json=tweet_list_json, search_word_json=search_word_json)



""" MAKE SURE to DEBUG FALSE """

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0')
