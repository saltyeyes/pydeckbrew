import urllib, urllib2, json
from collections import defaultdict
from cards import Card

class DeckBrewError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

class Request(object):
    filter_types = {'status': str, 'set': str, 'name': str, 'format': str, 'color': str, 'multiverse': str, 'rarity': str, 'subtype': str, 'oracle': str, 'supertype': str, 'type': str, "multicolor":bool}
    def __init__(self, params={}):
        self.base_url = "https://api.deckbrew.com/mtg/cards"
        self.base_params = params
        self.reset()
    def reset(self):
        self.filters = defaultdict(set)
        self.all = []
        self.pages = {}
        self.next_page = 1
    def __download_page(self, opt_params):
        params = dict(self.base_params.items() + opt_params.items())
        if "page" not in params:
            params["page"] = 1
        url = self.base_url + "?" + urllib.urlencode(params.items() + [(k, i) for k, v in self.filters.items() for i in v])
        print url
        result = json.loads(urllib2.urlopen(url).read())
        if "errors" in result:
            raise DeckBrewError("Error: " + " - ".join(result["errors"]))
        cards = [Card(i) for i in result]
        self.pages[params["page"]] = cards
        self.all += cards
    def page(self, num=1):
        if num not in self.pages:
            self.__download_page({"page":num})
            if num == self.next_page:
                self.next_page += 1
        return self.pages[num]
    def next(self):
        return self.page(self.next_page)
    def filter(self, **kwargs):
        for k, v in kwargs.items():
            if k not in Request.filter_types:
                raise DeckBrewError("Invalid keyword argument: "+k)
            if type(v) != Request.filter_types[k]:
                raise DeckBrewError("Invalid type for keyword %s - expected %s, received %s"%(k, Request.filter_types[k], type(v)))
            self.filters[k].add(v)
        return self