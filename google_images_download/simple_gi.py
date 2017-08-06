#!/usr/bin/env python3
from urllib.parse import ParseResult, urlencode, urlparse, parse_qs
from bs4 import BeautifulSoup
import requests


def parse_page(html):
    soup = BeautifulSoup(html, 'html5lib')
    a_tags = soup.select('div a')
    for tag in a_tags:
        href = tag.attrs['href']
        query_string = urlparse(href).query
        query_dict = parse_qs(query_string)
        yield query_dict['imgurl'][0]


class Session:

    def __init__(self):
        self.session = requests.Session()

    def get_page(self, query, page=0):
        url_query = {
            'q': query, 'tbm': 'isch', 'ijn': str(page), 'start': str(page * 100),
            'asearch': 'ichunk', 'async': '_id:rg_s,_pms:s'
        }
        url = ParseResult(
            scheme='https', netloc='google.com', path='/search', params=None,
            query=urlencode(url_query), fragment=None
        ).geturl()
        resp = self.session.get(url)
        return resp.json()[1][1]

    def get_images(self, query, limit=1):
        assert limit > 0
        result = []
        page = 0
        while len(result) < limit:
            page_html = self.get_page(query=query, page=page)
            result.extend(parse_page(page_html))
            page += 1
        return result


if __name__ == '__main__':
    # example
    session = Session()
    imgs = session.get_images('red swimsuit', 500)
    print('\n'.join(imgs))
