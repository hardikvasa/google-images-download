#!/usr/bin/env python3
from urllib.parse import ParseResult, urlencode, urlparse, parse_qs
from bs4 import BeautifulSoup
import requests


def parse_page(html):
    """Parse page."""
    soup = BeautifulSoup(html, 'html5lib')
    a_tags = soup.select('div a')
    for tag in a_tags:
        href = tag.attrs['href']
        query_string = urlparse(href).query
        query_dict = parse_qs(query_string)
        yield query_dict['imgurl'][0]


def get_json_resp_query_url(query, page):
    """Get url to get json response."""
    url_query = {
        'q': query, 'tbm': 'isch', 'ijn': str(page), 'start': str(page * 100),
        'asearch': 'ichunk', 'async': '_id:rg_s,_pms:s'
    }
    return ParseResult(
        scheme='https', netloc='google.com', path='/search', params=None,
        query=urlencode(url_query), fragment=None
    ).geturl()


def get_json_resp(query, page=0, req_func=None, return_url=False):
    """get json response."""
    url = get_json_resp_query_url(query, page)
    if req_func is None:
        req = requests
        resp = req.get(url)
        response_result = resp.json()[1][1]
    else:
        response_result = req_func(url)
    if return_url:
        return response_result, url
    return response_result


class Session:
    """Session."""

    def __init__(self):
        self.session = requests.Session()

    def get_page(self, query, page=0):
        """Get page."""
        def get_response(url):
            """Get respone func to get json response."""
            resp = self.session.get(url)
            return resp.json()[1][1]
        return get_json_resp(query, page=page, req_func=get_response)

    def get_images(self, query, limit=1):
        """get images.

        >>> session = Session()
        >>> imgs = session.get_images('red swimsuit', 500)
        >>> print('\n'.join(imgs))
        """
        assert limit > 0
        result = []
        page = 0
        while len(result) < limit:
            page_html = self.get_page(query=query, page=page)
            result.extend(parse_page(page_html))
            page += 1
        return result
