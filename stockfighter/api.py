import json
import requests
from urllib.parse import urljoin

class Resource(object):
    def __init__(self, session, *url_parts):
        self.session = session
        self.url_parts = url_parts
        self.url = '/'.join(url_parts)
    
    def _parse(self, response):
        response.raise_for_status()
        json = response.json()
        if json['ok'] is not True:
            raise Exception(json)
        return json
            
    def get(self):
        response = self.session.get(self.url)
        return self._parse(response)
                
    def post(self, data={}):
        response = self.session.post(self.url, json=data)
        return self._parse(response)
        
    def descend(self, *url_parts):
        return Resource(self.session, *(self.url_parts + url_parts))


class Session(object):
    def __init__(self, api_key):
        session = requests.Session()
        session.headers = {
            'X-Starfighter-Authorization': api_key
        }
        self.gm = Gamemaster(session)
        self.sf = Stockfighter(session)


class ResourceList(object):
    def __init__(self, parent, url_part, clazz, **kwargs):
        self.resource = parent.descend(url_part)
        self.clazz = clazz
        self.kwargs = kwargs
        
    # def __iter__(self):
    #     response = self.api.descend('/stocks').get()
    #     for stock in response['symbols']:
    #         yield Stock(self.api, self.venue, stock['symbol'])
        
    def __getitem__(self, key):
        return self.clazz(self.resource, key, **self.kwargs)


class Gamemaster(object):
    def __init__(self, session):
        resource = Resource(session, 'https://www.stockfighter.io', 'gm')
        self.levels = ResourceList(resource, 'levels', Level)
        self.instances = ResourceList(resource, 'instances', Instance)


class Level(object):
    def __init__(self, parent, name):
        self.resource = parent.descend(name)
    
    def start(self):
        return self.resource.post()


class Instance(object):
    def __init__(self, parent, id):
        self.resource = parent.descend(str(id))
        
    def get(self):
        return self.resource.get()
        
    def restart(self):
        return self.resource.descend('restart').post()
    
    def stop(self):
        return self.resource.descend('stop').post()
        
    def resume(self):
        return self.resource.descend('resume').post()


class Stockfighter(object):
    def __init__(self, session):
        self.resource = Resource(session, 'https://api.stockfighter.io', 'ob', 'api')
        self.venues = ResourceList(self.resource, 'venues', Venue)
    
    def heartbeat(self):
        return self.resource.descend('heartbeat').get()


class Venue(object):
    def __init__(self, parent, symbol):
        self.resource = parent.descend(symbol)
        self.symbol = symbol
        self.stocks = ResourceList(self.resource, 'stocks', Stock, venue=self)
        
    def heartbeat(self):
        return self.resource.descend('heartbeat').get()
                
    def __str__(self):
        return self.symbol


class Stock(object):
    def __init__(self, parent, symbol, venue):
        self.resource = parent.descend(symbol)
        self.symbol = symbol
        self.venue = venue
        
    def quote(self):
        return self.resource.descend('quote').get()
        
    def buy(self, account, price, qty, order_type='limit'):
        return self.resource.descend('orders').post({
            'account': account,
            'venue': self.venue.symbol,
            'symbol': self.symbol,
            'price': price,
            'qty': qty,
            'direction': 'buy',
            'orderType': order_type
        })
        
    def __str__(self):
        return "{0!s}:{1}".format(self.venue, self.symbol)