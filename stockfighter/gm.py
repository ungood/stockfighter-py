import requests

from stockfighter import api

class Gamemaster(object):
    def __init__(self, api_key):
       session = requests.Session()
       requests.utils.add_dict_to_cookiejar(session.cookies, {
           'api_key': api_key
       }) 
       
       self.api = api.Api(session, 'https://www.stockfighter.io/gm')
       
       self.levels = Levels(self.api)


def get_levels(api_key):
    session = requests.Session()
    session.headers = {
        'X-Starfighter-Authorization': api_key,
        'Content-Type': 'text/json'
    }
    
    f = api.Api(session, 'https://www.stockfighter.io/ui')
    
    return session.get('https://www.stockfighter.io/ui/levels').content


class Levels(object):
    def __init__(self, api):
        self.api = api
    
    def __iter__(self):
        response = self.api.descend('/levels').get()
        print(response)
        yield "hi"
#        for stock in response['symbols']:
 #           yield Stock(self.api, self.venue, stock['symbol'])
    
    def __getitem__(self, name):
        return Level(self.api, name)

class Level(object):
    def __init__(self, api, name):
        self.api = api.descend('/levels/' + name)
    
    def start(self):
        return self.api.post()