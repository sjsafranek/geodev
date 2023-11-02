import requests
# from bs4 import BeautifulSoup

import version


def get_headers(headers):
    headers = headers if headers is not None else {}
    headers['User-Agent'] = f'{version.TITLE}/{version.VERSION}'
    return headers


class HttpClient(object):

    def __init__(self, base_url):
        # Reuse tcp/http connections
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, endpoint, headers=None, params=None):
        uri = '{0}{1}'.format(self.base_url, endpoint)
        headers = get_headers(headers)
        return self.session.get(uri, headers=headers, params=params)

    def post(self, endpoint, headers=None, params=None, json=None):
        uri = '{0}{1}'.format(self.base_url, endpoint)
        headers = get_headers(headers)
        return self.session.post(uri, headers=headers, params=params, json=json)

    # def getHTML(self, endpoint, **kwargs):
    #     return BeautifulSoup(
    #                 self.get(endpoint, **kwargs).text,
    #                 'html.parser')

    def getJSON(self, endpoint, **kwargs):
        return self.get(endpoint, **kwargs).json()

    def postJSON(self, endpoint, **kwargs):
        return self.post(endpoint, **kwargs).json()        