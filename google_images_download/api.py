#!/usr/bin/python3
from urllib.parse import urlparse, urlencode, parse_qs, urljoin, quote_plus
import shutil
import json
import tempfile
import os

from bs4 import BeautifulSoup
from PIL import Image
import requests
import structlog

import google_images_download as gid
from google_images_download.sha256 import sha256_checksum

log = structlog.getLogger(__name__)


def get_or_create_search_query(query, page=1, disable_cache=False):
    """Get or create search_query."""
    url_page = page - 1
    url_query = {
        'q': query, 'tbm': 'isch', 'ijn': str(url_page),
        'start': str(int(url_page) * 100),
        'asearch': 'ichunk', 'async': '_id:rg_s,_pms:s'
    }
    parsed_url = urlparse('https://www.google.com/search')
    query_url = parsed_url._replace(query=urlencode(url_query)).geturl()
    kwargs = {'search_query': query, 'page': page}
    model, created = gid.models.get_or_create(
        gid.models.db.session, gid.models.SearchQuery, **kwargs)
    log.debug(
        'SearchQuery', sq_id=model.id, page=page, created=created, cache_disabled=disable_cache)
    if created or disable_cache:
        log.debug('query url', url=query_url)
        resp = requests.get(query_url)
        json_resp = resp.json()
        match_result_ms = []
        match_result_sets = get_or_create_match_result_from_json_resp(
            json_resp, search_query=model)
        for match_result_m, match_result_m_created in match_result_sets:
            match_result_ms.append(match_result_m)
        model.match_results.extend(match_result_ms)
    return model, created


def parse_match_result_html_tag(html_tag):
    """Get or create match result from json response"""
    kwargs = {'imgres_url': html_tag.select_one('a').get('href', None)}
    kwargs['imgref_url'] = parse_qs(
        urlparse(kwargs['imgres_url']).query).get('imgrefurl', [None])[0]

    # json data
    json_data = json.loads(html_tag.select_one('.rg_meta').text)
    if 'msu' in json_data and json_data['msu'] != json_data['si']:
        log.warning(
            "msu-value different with si-value", msu=json_data['msu'], si=json_data['si'])
    kwargs['json_data'] = json_data

    # image url
    imgres_url_query = parse_qs(urlparse(kwargs['imgres_url']).query)
    if imgres_url_query:
        url_from_img_url = imgres_url_query.get('imgurl', [None])[0]
        img_url_width = int(imgres_url_query.get('w', [None])[0])
        img_url_height = int(imgres_url_query.get('h', [None])[0])
    else:
        url_from_img_url = json_data['ou']
        img_url_width = int(json_data['ow'])
        img_url_height = int(json_data['oh'])
    kwargs['img_url'] = {
        'url': url_from_img_url,
        'width': img_url_width,
        'height': img_url_height
    }

    # add tags to image url
    img_url_tags = [
        {'namespace': 'picture title', 'name': json_data['pt']},
        {'namespace': 'site', 'name': json_data['isu']},
    ]
    if 'st' in json_data:
        img_url_tags.append({'namespace': 'site title', 'name': json_data['st']})
    if 'ru' in json_data:
        img_url_tags.append({'namespace': 'image page url', 'name': json_data['ru']})
    picture_subtitle = json_data.get('s', None)
    if picture_subtitle:
        img_url_tags.append({'namespace': 'picture subtitle', 'name': picture_subtitle})
    img_ext = json_data.get('ity', None)
    if img_ext:
        img_url_tags.append({'namespace': 'img ext', 'name': img_ext})
    kwargs['img_url_tags'] = img_url_tags

    # thumbnail url
    kwargs['thumbnail_url'] = {
        'url': json_data['tu'],
        'width': int(json_data['tw']),
        'height': int(json_data['th']),
    }
    return kwargs


def get_or_create_image_url_from_dict(dict_input):
    """Get or create match result from json response"""
    model, created = gid.models.get_or_create(
        gid.models.db.session, gid.models.ImageURL, url=dict_input['url'])
    size_exist = (dict_input['width'] or dict_input['height'])
    size_changed = False
    if created and size_exist:
        model.width = dict_input['width']
        model.height = dict_input['height']
        size_changed = True
    elif not created and size_exist:
        if not model.width and dict_input['width']:
            model.width = dict_input['width']
            size_changed = True
        if not model.height and dict_input['height']:
            model.width = dict_input['height']
            size_changed = True
    if size_changed:
        gid.models.db.session.add(model)
    return model, created


def get_or_create_match_result_from_html_soup(html_tag, search_query=None):
    """Get or create match result from html_soup"""
    kwargs = parse_match_result_html_tag(html_tag)
    kwargs['json_data'] = json_data = gid.models.get_or_create(
        gid.models.db.session, gid.models.JSONData, value=kwargs['json_data'])[0]
    kwargs['json_data_id'] = json_data.id
    # image url
    kwargs['img_url'] = img_url = get_or_create_image_url_from_dict(kwargs['img_url'])[0]
    kwargs['thumbnail_url'] = thumbnail_url = \
        get_or_create_image_url_from_dict(kwargs['thumbnail_url'])[0]
    add_tags_to_image_url(img_url, kwargs.pop('img_url_tags', []))

    # id
    kwargs['img_url_id'] = img_url.id
    kwargs['thumbnail_url_id'] = thumbnail_url.id
    # optional search_query
    if search_query:
        kwargs['search_query'] = search_query
    if not search_query:
        model, created = gid.models.get_or_create(
            gid.models.db.session, gid.models.MatchResult, **kwargs)
    else:
        new_kwargs = {
            'search_query': search_query,
            'img_url': img_url,
            'thumbnail_url': thumbnail_url,
        }
        model, created = gid.models.get_or_create(
            gid.models.db.session, gid.models.MatchResult, **new_kwargs)
        for key, value in kwargs.items():
            setattr(model, key, value)
    return model, created


def get_or_create_match_result_from_json_resp(json_resp, search_query=None):
    """Get or create match result from json response"""
    html = json_resp[1][1]
    soup = BeautifulSoup(html, 'html.parser')
    for html_tag in soup.select('.rg_bx'):
        model, create = get_or_create_match_result_from_html_soup(html_tag, search_query)
        yield model, create


def add_tags_to_image_url(img_url, tags):
    """add tags to image url."""
    tags_models = []
    for tag in tags:
        if not tag['name']:
            log.debug('tag only contain namespace', namespace=tag['namespace'])
        # with gid.models.db.session.no_autoflush:
        tag_m, _ = gid.models.get_or_create(
            gid.models.db.session, gid.models.Tag, **tag)
        if tag_m not in img_url.tags:
            img_url.tags.append(tag_m)
        tags_models.append(tag_m)
    return tags_models


def get_html_text_from_search_url(search_url=None, url=None):
    """Get HTML text from search url"""
    if not((search_url or url) and not (search_url and url)):
        raise ValueError('search url or image url only')
    user_agent_dict = {
        'firefox': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',  # NOQA
        'chrome': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',  # NOQA
    }
    headers = {'User-Agent': user_agent_dict['firefox']}
    url_templ = 'https://www.google.com/searchbyimage?image_url={}&safe=off'
    if search_url:
        resp = requests.get(search_url, headers=headers, timeout=10)
    elif url:
        search_url_from_image = url_templ.format(quote_plus(url))
        resp = requests.get(search_url_from_image, headers=headers, timeout=10)
        search_url = resp.url
    else:
        raise ValueError('Unknown condition, search url: {} url: {}'.format(search_url, url))
    html_text = resp.text
    keyword_text = 'Our systems have detected unusual traffic from your computer network.'
    if keyword_text in resp.text:
        log.debug('get html with different user agent')
        new_headers = {'User-Agent': user_agent_dict['chrome']}
        if search_url:
            resp = requests.get(search_url, headers=new_headers, timeout=10)
        else:
            resp = requests.get(search_url_from_image, headers=new_headers, timeout=10)
            search_url = resp.url
        if keyword_text in resp.text:
            templ = 'Unusual traffic detected, response status code:{}'
            err_msg = templ.format(resp.status_code)
            log.error(err_msg)
            raise ValueError(err_msg)
        html_text = resp.text
    return {'html_text': html_text, 'search_url': search_url}


def get_search_image_result_html(file_path=None, url=None):
    """get search image result."""
    if not((file_path or url) and not (file_path and url)):
        raise ValueError('input url or file_path only')
    kwargs = {}
    if file_path:
        search_url = 'http://www.google.com/searchbyimage/upload'
        multipart = {'encoded_image': (file_path, open(file_path, 'rb')), 'image_content': ''}
        response = requests.post(search_url, files=multipart, allow_redirects=False)
        kwargs = {'search_url': response.headers['Location']}
        kwargs.update(get_html_text_from_search_url(search_url=kwargs['search_url']))
    elif url:
        kwargs.update(get_html_text_from_search_url(url=url))
    else:
        raise ValueError('Unknown condition, file path: {} url: {}'.format(file_path, url))
    return kwargs


def get_or_create_search_image(file_path=None, url=None, disable_cache=False, thumb_folder=None):
    """get match result from file."""
    if not((file_path or url) and not (file_path and url)):
        raise ValueError('input url or file_path only')
    if file_path:
        img_file, _ = get_or_create_image_file_with_thumbnail(
            file_path, disable_cache=disable_cache, thumb_folder=thumb_folder)
        model, created = gid.models.get_or_create(
            gid.models.db.session, gid.models.SearchImage, img_file=img_file)
    elif url:
        instance = gid.models.SearchImage.query.filter_by(searched_img_url=url).first()
        if not instance:
            search_image_result_html_dict = get_search_image_result_html(url=url)
            html_text = search_image_result_html_dict['html_text']
            search_url = search_image_result_html_dict['search_url']
            instance = gid.models.SearchImage.query.filter_by(searched_img_url=url).first()
            if not instance:
                model, created = gid.models.get_or_create(
                    gid.models.db.session, gid.models.SearchImage,
                    search_url=search_url, searched_img_url=url
                )
            else:
                model = instance
                created = False
            model.searched_img_url = url
        else:
            model = instance
            created = False
    else:
        raise ValueError('Unknown condition, file path: {} url: {}'.format(file_path, url))
    if created or disable_cache:
        if file_path:
            search_image_result_html_dict = get_search_image_result_html(file_path=file_path)
        elif url:
            search_image_result_html_dict = get_search_image_result_html(url=url)
        html_text = search_image_result_html_dict['html_text']
        search_url = search_image_result_html_dict['search_url']
        kwargs = {'search_url': search_url}
        search_page = BeautifulSoup(html_text, 'lxml')
        base_url = 'https://www.google.com'
        # parsing: size_search_url
        size_search_tag = search_page.select_one('._v6 .gl a')
        if size_search_tag:
            size_search_url = size_search_tag.attrs.get('href', None)
            if size_search_url:
                kwargs['size_search_url'] = urljoin(base_url, size_search_url)
        # parsing: similar search url
        similar_search_tag = search_page.select_one('h3._DM a')
        if similar_search_tag:
            similar_search_url = similar_search_tag.attrs.get('href', None)
            if similar_search_url:
                kwargs['similar_search_url'] = urljoin(base_url, similar_search_url)
        # parsing: image guess
        image_guess_tag = search_page.select_one('._hUb a')
        if image_guess_tag:
            kwargs['img_guess'] = image_guess_tag.text
        # parsing: main similar result
        main_similar_tags = search_page.select('.rg_ul .rg_el')
        msr_models = []
        if main_similar_tags:
            for tag in main_similar_tags:
                msr_kwargs = {}
                msr_kwargs['search_url'] = tag.select_one('a').attrs.get('href', None)
                img_tag = tag.select_one('img')
                msr_kwargs['img_src'] = img_tag.attrs.get('src', None)
                msr_kwargs['img_width'] = img_tag.attrs.get('width', None)
                msr_kwargs['img_height'] = img_tag.attrs.get('height', None)
                msr_kwargs['img_title'] = img_tag.attrs.get('title', None)
                msr_model, _ = gid.models.get_or_create(
                    gid.models.db.session, gid.models.MainSimilarResult, **msr_kwargs)
                msr_models.append(msr_model)
        # parsing: text match parsing
        text_match_tags = search_page.select('._NId > .srg > .g')
        tm_models = []
        if text_match_tags:
            for tag in text_match_tags:
                tm_model_kwargs = parse_text_match_html_tag(tag)
                tm_model, _ = gid.models.get_or_create(
                    gid.models.db.session, gid.models.TextMatch, **tm_model_kwargs)
                tm_models.append(tm_model)
        # END: parsing
        for key, value in kwargs.items():
            setattr(model, key, value)
        if msr_models:
            model.main_similar_results.extend(msr_models)
        if tm_models:
            model.text_matches.extend(tm_models)
    return model, created


def parse_text_match_html_tag(html_tag):
    """Parse text match html tag."""
    kwargs = {}
    kwargs['title'] = html_tag.select_one('h3').text
    kwargs['url'] = html_tag.select_one('h3 a').attrs.get('href', None)
    kwargs['url_text'] = html_tag.select_one('.f cite').text
    kwargs['text'] = html_tag.select_one('.st').text
    img_tag = html_tag.select_one('img')
    if img_tag:
        # TODO
        log.warning('Image tag found, but no parser implemented yet.')
        pass
    return kwargs


def get_or_create_page_search_image(file_path=None, url=None, **kwargs):
    """Get or create page from search image.

    Args:
        **search_type: search type.
        **page: page.
        **disable_cache: disable_cache.

    """
    search_type = kwargs.get('search_type')
    page = kwargs.get('page', 1)
    disable_cache = kwargs.get('disable_cache', False)
    if page > 1:
        raise NotImplementedError('Only first page implemented yet.')
    if not((file_path or url) and not (file_path and url)):
        raise ValueError('input url or file_path only')
    sm_model, _ = get_or_create_search_image(file_path, url=url, disable_cache=disable_cache)
    kwargs = {'search_img': sm_model, 'search_type': search_type, 'page': page}
    model, created = gid.models.get_or_create(
        gid.models.db.session, gid.models.SearchImagePage, **kwargs
    )
    if created or disable_cache:
        gr_url = None
        if gid.models.SearchImagePage.TYPE_SIMILAR == search_type:
            gr_url = sm_model.similar_search_url
        elif gid.models.SearchImagePage.TYPE_SIZE == search_type:
            gr_url = sm_model.size_search_url
        else:
            log.error('Unknown search type: {}'.format(search_type))
        if not gr_url:
            gid.models.db.session.add(sm_model)
            gid.models.db.session.commit()
            raise ValueError('No url found for search type: {}'.format(search_type))
        user_agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1'  # NOQA
        resp = requests.get(gr_url, headers={'User-Agent': user_agent}, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        mr_models = []
        for html_tag in soup.select('.rg_bx'):
            mr_model, _ = get_or_create_match_result_from_html_soup(html_tag)
            mr_models.append(mr_model)
        model.match_results.extend(mr_models)
    return model, created


def get_or_create_image_file_with_thumbnail(file_path, disable_cache=False, thumb_folder=None):
    """Get or create image file with thumbnail."""
    thumb_folder = thumb_folder if thumb_folder else gid.models.DEFAULT_THUMB_FOLDER
    img_file, img_file_created = get_or_create_image_file(file_path, disable_cache=disable_cache)
    is_thumbnail_exist = False
    file_path_eq_thumb_path = False
    if img_file.thumbnail:
        thumbnail_path = os.path.join(thumb_folder, img_file.thumbnail.checksum + '.jpg')
        is_thumbnail_exist = os.path.isfile(thumbnail_path)
        file_path_eq_thumb_path = file_path == thumbnail_path
    if not is_thumbnail_exist and file_path_eq_thumb_path:
        img_file.thumbnail = img_file
    elif not is_thumbnail_exist:
        thumbnail_file = create_thumbnail(file_path, thumb_folder)
        log.debug('thumbnail created', m=thumbnail_file, folder=thumb_folder)
        thumbnail_file_model, _ = \
            get_or_create_image_file(thumbnail_file, disable_cache=disable_cache)
        thumbnail_file_model.thumbnail = thumbnail_file_model
        img_file.thumbnail = thumbnail_file_model
    return img_file, img_file_created


def get_or_create_image_file(file_path, disable_cache=False):
    """Get image file."""
    checksum = sha256_checksum(file_path)
    model, created = gid.models.get_or_create(
        gid.models.db.session, gid.models.ImageFile, checksum=checksum)
    if created or disable_cache:
        kwargs = {}
        img = Image.open(file_path)
        kwargs['width'] = img.size[0]
        kwargs['height'] = img.size[1]
        kwargs['img_format'] = img.format
        kwargs['size'] = os.path.getsize(file_path)
        for key, value in kwargs.items():
            setattr(model, key, value)
    return model, created


def create_thumbnail(file_path, thumbnail_folder):
    with tempfile.NamedTemporaryFile() as temp:
        img = Image.open(file_path)
        size = (256, 256)
        img.thumbnail(size)
        try:
            img.save(temp.name, 'JPEG')
        except OSError as err:
            log.warning('Error create thumbnail, convert to jpg first', error=err)
            img.convert('RGB').save(temp.name, 'JPEG')
        thumb_checksum = gid.sha256.sha256_checksum(temp.name)
        thumbnail_path = os.path.join(thumbnail_folder, thumb_checksum + '.jpg')
        if not os.path.isfile(thumbnail_path):
            shutil.copyfile(temp.name, thumbnail_path)
        return thumbnail_path
