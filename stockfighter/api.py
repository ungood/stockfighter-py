import json
import requests

def validate(response):
    response.raise_for_status()
    json = response.json()
    if json['ok'] is not True:
        raise Exception(json)
    return json

class Api(object):
    def __init__(self, session, url):
        self.session = session
        self.url = url
    
    def descend(self, path):
        return Api(self.session, self.url + path)
    
    def get(self):
        # self.log.debug(url)
        return validate(self.session.get(self.url))
                
    def post(self, data={}):
        return validate(self.session.post(self.url, json=data))    