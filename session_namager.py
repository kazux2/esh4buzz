# coding: UTF-8


from json import JSONEncoder, JSONDecoder
from tweepy import API


class SessionManager(JSONEncoder, JSONDecoder, API):

    def default(self , obj) :
        if isinstance(obj, API):  # NotSettedParameterは'NotSettedParameter'としてエンコード
            return 'NotSettedParameter'
        return JSONEncoder.default(self, obj)  # 他の型はdefaultのエンコード方式を使用
