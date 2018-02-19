# coding: UTF-8


from json import JSONEncoder, JSONDecoder
from tweepy import API


class SessionManager(JSONEncoder, JSONDecoder, API):

    def default(self , obj) :
        if isinstance(obj, API):  # APIは'API'としてエンコード
            return 'API'
        return JSONEncoder.default(self, obj)  # 他の型はdefaultのエンコード方式を使用
