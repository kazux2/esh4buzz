# coding: UTF-8

import logging
from flask import Flask, redirect, render_template, request, url_for
from NLP import NLP
import tweepy
from twitter_search import TwitterSearch
from data_formatter import JsonFormatter
from settings import SETTING, SETTING0


CONSUMER_KEY    = SETTING['twitter']['CONSUMER_KEY']
CONSUMER_SECRET = SETTING['twitter']['CONSUMER_SECRET']
CALLBACK_URL    = SETTING['twitter']['CALLBACK_URL']

CONSUMER_KEY0 = SETTING0['twitter']['CONSUMER_KEY']

session = dict()

app = Flask(__name__)
app.secret_key = SETTING['flask']['SECRET_KEY']


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
        session['request_token'] = (auth.request_token)

    except tweepy.TweepError:
        print('Error! Failed to get request token')

    return redirect(redirect_url)


@app.route("/verify")
def verify():

    verifier = request.args['oauth_verifier']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    token = session['request_token']
    # del session['request_token']

    auth.request_token = {'oauth_token': token['oauth_token'],
                          'oauth_token_secret': token['oauth_token_secret']}
    del token


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
    global session
    if request.method == 'POST':

        query = request.form["target_text"]

        nlp = NLP()
        twitter_search = TwitterSearch()

        count_query = nlp.count_segmentation(query)
        count = nlp.capacity_check(count_query)


        if count:

            json_formatter = JsonFormatter()

            twitter_search.session_receiver(session)

            search_word_dict = nlp.text_segmentation(query, 99, 3) #query, limit, accuracy
            search_word_json = json_formatter.search_dict_to_json(search_word_dict)

            tweet_list_json = json_formatter.execute_basics(search_word_dict)

            # premiere account function
            # json_formatter.save_result_tweet('json_data/result_tweet_json8.json', tweet_list_json)
            # tweet_list_json = json_formatter.load_search_result('json_data/result_tweet_json8.json')


            return render_template("result.html", tweet_list_json = tweet_list_json, search_word_json = search_word_json)

        else:
            return render_template("search_failed.html", jsonn={'message':'either query is too long or too short dayo'})


""" MAKE SURE DEBUG FALSE """

if __name__ == '__main__':
    app.debug = False # when deploy debug False
    app.run(host='0.0.0.0')
