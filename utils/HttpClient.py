
import requests
# from bs4 import BeautifulSoup
from functools import lru_cache

#from logger import logger


class HttpClient(object):

    def __init__(self, base_url):
        # Reuse tcp/http connections
        self.base_url = base_url
        self.session = requests.Session()

    #@lru_cache(maxsize=120)
    def get(self, endpoint, headers=None, params=None):
        uri = '{0}{1}'.format(self.base_url, endpoint)
        return self.session.get(uri, headers=headers, params=params)

    # def getHTML(self, endpoint, **kwargs):
    #     return BeautifulSoup(
    #                 self.get(endpoint, **kwargs).text,
    #                 'html.parser')

    def getJSON(self, endpoint, **kwargs):
        return self.get(endpoint, **kwargs).json()