import requests, json
import logging
import os

    
    
class Stockfighter(object):
    def __init__(self, api_key):
        if api_key is None:
            api_key = os.environ['API_KEY']
        
        ob_session = requests.Session()
        ob_session.headers = {
            'X-Starfighter-Authorization': api_key
        }
        
        gm_session = requests.Session()
        requests.utils.add_dict_to_cookiejar(gm_session.cookies, {
            'api_key': api_key
        })
        
        self.ob = Api(ob_session, 'https://api.stockfighter.io/ob/api')        
        self.gm = Api(ob_session, 'https://www.stockfighter.io/gm')
        self.levels = Levels(self.gm)
        self.venues = Venues(self.ob)
    
    def heartbeat(self):
        return self.ob.descend('/heartbeat').get()
                

        
class Venues(object):
    def __init__(self, api):
        self.api = api
        
    def __getitem__(self, symbol):
        return Venue(self.api, symbol)

class Venue(object):
    def __init__(self, api, symbol):
        self.api = api.descend('/venues/' + symbol)
        self.symbol = symbol
        self.stocks = Stocks(self.api, self)
        
    def heartbeat(self):
        return self.api.descend('/heartbeat').get()
                
    def __str__(self):
        return self.symbol
        
class Stocks(object):
    def __init__(self, api, venue):
        self.api = api
        self.venue = venue
        
    def __iter__(self):
        response = self.api.descend('/stocks').get()
        for stock in response['symbols']:
            yield Stock(self.api, self.venue, stock['symbol'])
    
    def __getitem__(self, symbol):
        return Stock(self.api, self.venue, symbol)
        
class Stock(object):
    def __init__(self, api, venue, symbol):
        self.api = api.descend('/stocks/' + symbol)
        self.venue = venue
        self.symbol = symbol
        
    def quote(self):
        return self.api.descend('/quote').get()
        
    def buy(self, account, price, qty, order_type='limit'):
        return self.api.descend('/orders').post({
            'account': account,
            'venue': self.venue.symbol,
            'symbol': self.symbol,
            'price': price,
            'qty': qty,
            'direction': 'buy',
            'orderType': order_type
        })
        
    def __str__(self):
        return "{0!s}: {1}".format(self.venue, self.symbol)