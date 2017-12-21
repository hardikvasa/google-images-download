#!/usr/bin/env python3
"""google image related function.

modified version from
http://stackoverflow.com/a/28792943
"""
import json
import webbrowser
from datetime import datetime
from pprint import pprint
from urllib.parse import urljoin

import requests
import structlog
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


log = structlog.getLogger(__name__)


def get_default_session():
    ua = UserAgent()
    session = requests.Session()
    session.headers.update({'User-Agent': ua.firefox})
    return session


def get_post_response(file_path, session=None, return_mode='response'):
    """Get post response."""
    session = session if session is not None else get_default_session()
    search_url = 'http://www.google.com/searchbyimage/upload'
    multipart = {'encoded_image': (file_path, open(file_path, 'rb')), 'image_content': ''}
    response = session.post(search_url, files=multipart, allow_redirects=False)
    if return_mode == 'url':
        return response.headers['Location']
    else:
        return response


def get_first_page_data(soup):
    """Get first page data from location url."""
    res = {
        'best_guess': {},
        'other_size': {},
        'page_results': [],
        'pages_with_matching_image': [],
        'visually_similar_image_item': [],
        'visually_similar_image_link': None,
    }
    # link to other size
    for a_tag in soup.select('._v6 span.gl a'):
        res.setdefault('other_size', {}).update(
            {a_tag.text: a_tag.attrs.get('href', None)})
    # best guess
    bg_tag = soup.select('div.card-section a')
    if bg_tag:
        bg_tag = bg_tag[-1]
        res['best_guess'] = {bg_tag.text: bg_tag.attrs.get('href', None)}
    else:
        log.debug('Best guess section not found.')
    # page results
    h_div_tag = [x for x in soup.select('#rso .srg')]
    h_div_tag_len = len(h_div_tag)
    if h_div_tag_len == 0:
        log.debug('No match tag found for page results.')
    else:
        if not h_div_tag_len == 2:
            log.debug(
                'length of tag for page result parsing is unexpected',
                length=h_div_tag_len)
        h_div_tag = h_div_tag[0]
        for h_tag in h_div_tag.select('.g'):
            pr_item = {}
            pr_item['title'] = h_tag.select_one('h3 a')
            if pr_item['title']:
                pr_item['title'] = pr_item['title'].text
            pr_item['url'] = h_tag.select_one('h3 a').attrs.get('href', None)
            pr_item['data'] = h_tag.select_one('span.st .f')
            pr_item['data'] = pr_item['data'].text if pr_item['data'] else None
            pr_item['text'] = h_tag.select_one('span.st')
            if pr_item['text']:
                pr_item['text'] = h_tag.select_one('span.st').text
            if pr_item['data'] and pr_item['text']:
                pr_item['text'] = h_tag.select_one('span.st').text.replace(pr_item['data'], '', 1)
            res.setdefault('page_results', []).append(pr_item)
    # visually similar link
    res['visually_similar_image_link'] = soup.select_one('.iu-card-header')
    if res['visually_similar_image_link']:
        res['visually_similar_image_link'] = \
            res['visually_similar_image_link'].attrs.get('href', None)
    # visually_similar_image_item
    for h_tag in soup.select('.img-brk .rg_ul .uh_r'):
        vs_item = {}
        vs_item['link'] = h_tag.select_one('a').attrs.get('href', None)
        vs_item['img_src'] = h_tag.select_one('img').attrs.get('src', None)
        vs_item['img_title'] = h_tag.select_one('img').attrs.get('title', None)
        vs_item['json_data'] = h_tag.select_one('.rg_meta')
        if hasattr(vs_item['json_data'], 'text'):
            vs_item['json_data'] = json.loads(h_tag.select_one('.rg_meta').text)
        else:
            log.debug('Can\'t find json data text on div.rg_meta')
            vs_item['json_data'] = None
        res.setdefault('visually_similar_image_item', []).append(vs_item)
    # pages with matching image
    h_div_tag = [x for x in soup.select('#rso .srg')]
    h_div_tag_len = len(h_div_tag)
    if h_div_tag_len == 0:
        log.debug('No match tag found for page with matching image.')
    else:
        if not h_div_tag_len == 2:
            log.debug(
                'length of tag '
                'for page with matching image parsing is unexpected',
                length=h_div_tag_len)
        if h_div_tag_len == 1:
            log.debug('Use first tag section')
            h_div_tag = h_div_tag[0]
        else:
            h_div_tag = h_div_tag[1]
        for h_tag in h_div_tag.select('.g'):
            pmi_item = {}
            pmi_item['link'] = h_tag.select_one('a').attrs.get('href', None)
            pmi_item['title'] = h_tag.select_one('a').text
            pmi_item['text_data'] = h_tag.select_one('span.st .f')
            pmi_item['text'] = h_tag.select_one('span.st').text
            if pmi_item['text_data']:
                pmi_item['text_data'] = pmi_item['text_data'].text
                pmi_item['text'] = pmi_item['text'].replace(
                    pmi_item['text_data'], '', 1)
            pmi_item['img_src'] = h_tag.select_one('img')
            if hasattr(pmi_item['img_src'], 'attrs'):
                pmi_item['img_src'] = pmi_item['img_src'].attrs.get('src', None)
            else:
                log.debug('Can\'t find image source on img-tga')
                pmi_item['img_src'] = None
            res.setdefault('pages_with_matching_image', []).append(pmi_item)
    # pages link
    for h_tag in soup.select('table#nav a'):
        res.setdefault('pages_link', {}).update({
            h_tag.text: h_tag.attrs.get('href', None)})
    # logging
    log.debug('other size', n=len(res['other_size']))
    log.debug('best guess', bg=res['best_guess'])
    log.debug('page results', n=len(res['page_results']))
    if res['visually_similar_image_link']:
        log.debug(
            'visually similar image link',
            vsil=res['visually_similar_image_link'][:70] + '...'
        )
    else:
        log.debug('visually similar image link not found.')
    log.debug('visually similar image item', n=len(res['visually_similar_image_item']))
    log.debug('Page with matching image', n=len(res['pages_with_matching_image']))
    return res


def parse_image_page(soup):
    """Parse image page."""
    for h_tag in soup.select('.rg_bx'):
        item = {}
        item['size_txt'] = h_tag.select_one('span.rg_an').text
        json_data = json.loads(h_tag.select_one('.rg_meta').text)
        item['json_data'] = json_data
        item['pixel_size'] = int(json_data['oh']) * int(json_data['ow'])
        yield item


def get_largest_image(file_path, session, n_max_size=1):
    """Get largest image."""
    post_resp = get_post_response(file_path, session)
    post_resp_headers = post_resp.headers
    if 'Location' not in post_resp_headers:
        log.debug('Can\'t find location url', headers=post_resp_headers)
        return
    resp = session.get(post_resp.headers['Location'])
    soup = BeautifulSoup(resp.text, 'html.parser')

    try:
        res = get_first_page_data(soup)
    except IndexError as e:
        html_path = datetime.now().strftime("%Y%m%d-%H%M%S")
        html_path = 'dump_{}.html'.format(html_path)
        with open(html_path, 'w') as f:
            f.write(str(soup))
        log.error('Error, dump html.', e=str(e), html_path=html_path)
        raise e
    all_sizes_link = res['other_size'].get('All sizes', None)
    all_sizes_link = urljoin('https://google.com', all_sizes_link)
    as_link_resp = session.get(all_sizes_link)
    soup = BeautifulSoup(as_link_resp.text, 'html.parser')
    parsed_res = list(parse_image_page(soup))
    if not parsed_res:
        log.debug('No result found.')
        return
    elif n_max_size == 2:
        sizes = sorted((x['pixel_size'] for x in parsed_res), reverse=True)[:3]
        valid_pixel_sizes = sizes[:2]
    else:
        valid_pixel_sizes = [max([x['pixel_size'] for x in parsed_res])]
    valid_parsed_res = [
        x for x in parsed_res if x['pixel_size'] in valid_pixel_sizes]
    return valid_parsed_res


def get_first_page_data_from_file(file_path, session=None):
    session = session if session is not None else get_default_session()
    post_resp = get_post_response(file_path, session)
    post_resp_headers = post_resp.headers
    if 'Location' not in post_resp_headers:
        log.debug('Can\'t find location url', headers=post_resp_headers)
        return
    resp = session.get(post_resp.headers['Location'])
    soup = BeautifulSoup(resp.text, 'html.parser')

    return get_first_page_data(soup)


def search(file_path, mode='browser'):
    """Run simple program that search image."""
    session = get_default_session()
    if mode == 'data':
        res = get_first_page_data_from_file(file_path, session)
        pprint(res)
    elif mode in ('largest', 'largest-2size'):
        if mode == 'largest-2size':
            n_max_size = 2
        else:
            n_max_size = 1
        res = get_largest_image(file_path, session, n_max_size=n_max_size)
        if not res:
            print('No match found.')
            return
        for item in res:
            print('size:{}\n{}'.format(
                item['size_txt'], item['json_data']['ou']))
    else:
        fetch_url = get_post_response(file_path, session, 'url')
        webbrowser.open(fetch_url)
