# coding: UTF-8

import logging
from flask import Flask, redirect, render_template, request, url_for, session
import tweepy
from settings import SETTING
from timer import Timer
from session_namager import SessionManager
from text_segmentation import TextSegmentation
from twi_search import TwiSearch
from json_formatter import JsonFormatter
import mojimoji



CONSUMER_KEY    = SETTING['twitter']['CONSUMER_KEY']
CONSUMER_SECRET = SETTING['twitter']['CONSUMER_SECRET']
CALLBACK_URL    = SETTING['twitter']['CALLBACK_URL']

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
        session['request_token'] = (auth.request_token)
        # session.modified = True
        return redirect(redirect_url)

    except tweepy.TweepError:
        print('Error! Failed to get request token')



@app.route("/verify")
def verify():

    verifier = request.args['oauth_verifier']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.request_token = {'oauth_token': session['request_token']['oauth_token'],
                          'oauth_token_secret': session['request_token']['oauth_token_secret']}

    try:
        auth.get_access_token(verifier)

    except tweepy.TweepError:
        print('Error! Failed to get access token.')

    api = tweepy.API(auth)

    sm = SessionManager()
    session['api'] = sm.default(api)
    session['access_token_key'] = auth.access_token
    session['access_token_secret'] = auth.access_token_secret

    return redirect(url_for('search'))



@app.route("/search")
def search():
    return render_template("search.html")



@app.route("/result", methods=['post'])
def result():
    if request.method == 'POST':

        query = request.form["target_text"]
        ud_rate = request.form["ud_rate"]
        ud_rate_percent = float(ud_rate) / 100
        query  = mojimoji.zen_to_han(query, kana=False)

        txt_seg = TextSegmentation()
        r_dict           = txt_seg.segment_text(query, 99)       # query, limit
        r_dict_popped    = txt_seg.pop_search_words(ud_rate_percent, r_dict) #### #### routerからだとなぜか最後のループでdictの要素がlistで無くなる
        r_dict_joined    = txt_seg.join_dict_elements(r_dict_popped, 3) # minimum elements
        search_word_dict = txt_seg.reindex_r_dict(r_dict_joined)

        twi = TwiSearch(session)
        search_result = twi.make_search_result(search_word_dict)

        jf = JsonFormatter()
        init_tweet_list_json = jf.init_tweet_list_json(search_word_dict, search_result)
        search_word_json = jf.search_dict_to_json(search_word_dict)
        tweet_list_json = jf.input_tweet_list_json(search_word_dict, search_result, init_tweet_list_json)
        tweet_list_json = jf.del_empty_json(tweet_list_json, search_word_dict)

        # Save function
        # from model import Model
        # model = Model()
        # model.save_result_tweet('json_data/result_tweet_json8.json', tweet_list_json)
        # tweet_list_json = model.load_search_result('json_data/result_tweet_json8.json')

        return render_template("result.html", ud_rate = ud_rate, tweet_list_json=tweet_list_json, search_word_json=search_word_json)



""" MAKE SURE to DEBUG FALSE """

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0')
