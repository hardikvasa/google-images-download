#!/usr/bin/env python3
"""Model module."""
from datetime import datetime
from difflib import ndiff
from urllib.parse import urlparse, urljoin, urlencode, parse_qs
import json
import os
import shutil
import tempfile

from appdirs import user_data_dir
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP
from sqlalchemy_utils.types import URLType, JSONType, ChoiceType
import fake_useragent
import requests
import structlog

from google_images_download import sha256


log = structlog.getLogger(__name__)   # pylint: disable=invalid-name

db = SQLAlchemy()  # pylint: disable=invalid-name
search_query_match_results = db.Table(  # pylint: disable=invalid-name
    'match_results',
    db.Column(
        'match_result_id', db.Integer, db.ForeignKey('match_result.id'), primary_key=True),
    db.Column(
        'search_query_url', db.Integer, db.ForeignKey('search_query.query_url'), primary_key=True))
match_result_tags = db.Table(  # pylint: disable=invalid-name
    'match_result_tags',
    db.Column('match_result_id', db.Integer, db.ForeignKey('match_result.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.full_name'), primary_key=True))
search_query_tags = db.Table(  # pylint: disable=invalid-name
    'search_query_tags',
    db.Column(
        'search_query_url', db.Integer, db.ForeignKey('search_query.query_url'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.full_name'), primary_key=True))
image_url_tags = db.Table(  # pylint: disable=invalid-name
    'image_url_tags',
    db.Column('image_url_id', db.Integer, db.ForeignKey('imageURL.url'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.full_name'), primary_key=True))
search_model_tags = db.Table(  # pylint: disable=invalid-name
    db.Column(
        'search_model_id', db.Integer, db.ForeignKey('search_model.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.full_name'), primary_key=True))
search_model_match_results = db.Table(  # pylint: disable=invalid-name
    'search_model_match_results',
    db.Column('search_model_id', db.Integer, db.ForeignKey('search_model.id'), primary_key=True),
    db.Column('match_result_id', db.Integer, db.ForeignKey('match_result.id'), primary_key=True))

THUMB_FOLDER = os.path.join(user_data_dir('google_images_download', 'hardikvasa'), 'thumb')


def get_user_agent(browser='firefox'):
    """Get user agent."""
    user_agent = fake_useragent.UserAgent()
    try:
        return getattr(user_agent, browser)
    except fake_useragent.errors.FakeUserAgentError as err:
        log.error("Can't get useragent, use default", err=err)
        user_agent_dict = {
            'firefox': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) '
            'Gecko/20121011 Firefox/16.0.1',
            'chrome': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        }
        user_agent = \
            user_agent_dict['browser'] \
            if browser in user_agent_dict else user_agent_dict['firefox']
        return user_agent


class SearchQuery(db.Model):
    """Search query."""
    query_url = db.Column(URLType, primary_key=True)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    query = db.Column(db.String, nullable=False)
    page = db.Column(db.Integer)
    match_results = db.relationship(
        'MatchResult', secondary=search_query_match_results, lazy='subquery',
        backref=db.backref('search_query', lazy=True), enable_typechecks=False)
    tags = db.relationship(
        'Tag', secondary=search_query_tags, lazy='subquery',
        backref=db.backref('search_query', lazy=True), enable_typechecks=False)
    query_data = db.Column(JSONType)

    def __repr__(self):
        """Repr."""
        return '<Search query:[{}] page: {}>'.format(self.query, self.page)

    @staticmethod
    def get_or_create_from_query(query, page=1):
        """Get or create from query."""
        url_query = {
            'q': query, 'tbm': 'isch', 'ijn': str(page), 'start': str(int(page) * 100),
            'asearch': 'ichunk', 'async': '_id:rg_s,_pms:s'
        }
        parsed_url = urlparse('https://www.google.com/search')
        query_url = parsed_url._replace(query=urlencode(url_query)).geturl()
        kwargs = {'query': query, 'query_url': query_url, 'page': page}
        model, created = get_or_create(db.session, SearchQuery, **kwargs)
        return model, created

    def get_match_results(self):
        """Get match results."""
        if self.match_results:
            return self.match_results
        resp = requests.get(self.query_url)
        resp_json = resp.json()
        res = MatchResult.get_or_create_from_json_resp(resp_json)
        res_match_results = [x[0] for x in res]
        self.match_results.extend(res_match_results)
        db.session.add(self)  # pylint: disable=no-member
        db.session.commit()  # pylint: disable=no-member
        return res_match_results

    @property
    def google_url(self):
        """Get google url."""
        parsed_url = urlparse('https://www.google.com/search')
        url = parsed_url._replace(query=urlencode(self.query_data)).geturl()
        return url

    @staticmethod
    def get_or_create_from_google_url(url, page=1):
        """Get or create from google url."""
        # compatibility
        input_url = url

        input_url_query = parse_qs(urlparse(input_url).query)
        query = input_url_query.get('q', [None])[0]
        url_query = {
            'tbm': ['isch'], 'ijn': [str(page)], 'start': [str(int(page) * 100)],
            'asearch': ['ichunk'], 'async': ['_id:rg_s,_pms:s']
        }
        for key, value in url_query.items():
            if key in input_url_query and value == url_query[key]:
                if key != 'tbm':
                    log.debug('pop item', k=key)
                input_url_query.pop(key, None)
        url_query.update(input_url_query)
        parsed_url = urlparse('https://www.google.com/search')
        query_url = parsed_url._replace(query=urlencode(url_query, doseq=True)).geturl()
        input_url_query_json = json.dumps(input_url_query)
        kwargs = {
            'query': query, 'query_url': query_url, 'page': page,
            'query_data': input_url_query_json}
        model, created = get_or_create(db.session, SearchQuery, **kwargs)
        return model, created


class MatchResult(db.Model):
    """Match result."""
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    imgres_url = db.Column(URLType)
    imgref_url = db.Column(URLType)
    # column with valuew from json data
    json_data = db.Column(JSONType)
    json_data_id = db.Column(db.String)
    picture_title = db.Column(db.String)
    picture_subtitle = db.Column(db.String)
    site = db.Column(URLType)
    site_title = db.Column(db.String)
    image_page_url = db.Column(URLType)
    img_ext = db.Column(db.String)
    json_search_url = db.Column(db.String)
    # image and thumbnail
    img_url = db.Column(URLType, db.ForeignKey('imageURL.url'), nullable=False)
    thumb_url = db.Column(URLType, db.ForeignKey('imageURL.url'), nullable=False)
    image = db.relationship(
        'ImageURL', foreign_keys='MatchResult.img_url', lazy='subquery',
        backref=db.backref('match_results', lazy=True, cascade="delete"))
    thumbnail = relationship('ImageURL', foreign_keys='MatchResult.thumb_url', cascade="delete")
    # others
    tags = db.relationship(
        'Tag', secondary=match_result_tags, lazy='subquery',
        backref=db.backref('match_results', lazy=True))

    def __repr__(self):
        """Repr."""
        return '<Match result {}, site: {}, title: {}>'.format(
            self.id, self.site, self.picture_title)

    @staticmethod
    def get_or_create_from_json_resp(json_resp):
        """Get or create from json resp."""
        html = json_resp[1][1]
        soup = BeautifulSoup(html, 'html.parser')
        for html_tag in soup.select('.rg_bx'):
            model, created = MatchResult.get_or_create_from_html_tag(html_tag)
            yield (model, created)

    @staticmethod
    def get_or_create_from_html_tag(html_tag):
        """Get or create from html tag."""
        imgres_url = html_tag.select_one('a').get('href', None)
        imgref_url = parse_qs(
            urlparse(imgres_url).query).get('imgrefurl', [None])[0]
        json_data = json.loads(html_tag.select_one('.rg_meta').text)
        if 'msu' in json_data:
            if json_data['msu'] != json_data['si']:
                log.warning(
                    ''.join(ndiff([json_data['msu']], [json_data['si']])))
        kwargs = {
            'imgres_url': imgres_url,
            'imgref_url': imgref_url,
            # json data
            'json_data': json_data,
            'json_data_id': json_data['id'],
            'picture_title': json_data['pt'],
            'site': json_data['isu'],
            'site_title': json_data.get('st', None),
            'img_ext': json_data['ity'],
        }
        if 'msu' in json_data:
            kwargs['json_search_url'] = urljoin('https://www.google.com', json_data['msu'])

        if 'ru' in json_data:
            kwargs['image_page_url'] = json_data['ru']
        if 's' in json_data:
            kwargs['picture_subtitle'] = json_data['s']

        # img_url
        imgres_url_query = parse_qs(urlparse(imgres_url).query)
        if imgres_url_query:
            url_from_img_url = imgres_url_query.get('imgurl', [None])[0]
            img_url_kwargs = {
                'url': url_from_img_url,
                'width': int(imgres_url_query.get('w', [None])[0]),
                'height': int(imgres_url_query.get('h', [None])[0]),
            }
        else:
            url_from_img_url = json_data['ou']
            img_url_kwargs = {
                'url': url_from_img_url,
                'width': int(json_data['oh']),
                'height': int(json_data['ow']),
            }
        with db.session.no_autoflush:  # pylint: disable=no-member
            img_url, _ = get_or_create(db.session, ImageURL, **{'url': url_from_img_url})
        if img_url.height != img_url_kwargs['height']:
            img_url.height = img_url_kwargs['height']
        if img_url.width != img_url_kwargs['width']:
            img_url.width = img_url_kwargs['width']
        kwargs['image'] = img_url

        # thumb_url
        url_from_thumb_url = json_data['tu']
        thumb_url_kwargs = {
            'url': url_from_thumb_url,
            'width': int(json_data['tw']),
            'height': int(json_data['th']),
        }
        with db.session.no_autoflush:  # pylint: disable=no-member
            thumb_url, _ = get_or_create(db.session, ImageURL, **{'url': url_from_thumb_url})
        if thumb_url.height != thumb_url_kwargs['height']:
            thumb_url.height = thumb_url_kwargs['height']
        if thumb_url.width != thumb_url_kwargs['width']:
            thumb_url.width = thumb_url_kwargs['width']
        kwargs['thumbnail'] = thumb_url

        with db.session.no_autoflush:  # pylint: disable=no-member
            model, created = get_or_create(db.session, MatchResult, **kwargs)
        return model, created


class ImageURL(db.Model):
    """Image URL."""
    url = db.Column(URLType, primary_key=True)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    tags = db.relationship(
        'Tag', secondary=image_url_tags, lazy='subquery',
        backref=db.backref('image_urls', lazy=True))

    def __repr__(self):
        """Repr."""
        return '<{}>'.format(self.url)

    @property
    def basename(self):
        """Get image url filename."""
        return os.path.basename(urlparse(self.url).path)


class Tag(db.Model):
    """Tag model."""
    full_name = db.Column(db.String, primary_key=True)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @property
    def name(self):
        """Get tag name."""
        if ':' in self.full_name:
            return self.full_name.split(':', 1)[1]
        return self.full_name

    @property
    def namespace(self):
        """Get tag namespace."""
        if ':' in self.full_name:
            return self.full_name.split(':', 1)[0]


class ImageFile(db.Model):
    """Image file model."""
    checksum = db.Column(db.String, primary_key=True)  # pylint: disable=invalid-name
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    img_format = db.Column(db.String)
    size = db.Column(db.Integer)

    @staticmethod
    def get_or_create_from_file(file_path):
        """Get or create from file."""
        kwargs = {}
        checksum = sha256.sha256_checksum(file_path)
        model, created = get_or_create(
            db.session, ImageFile, checksum=checksum)
        if not created:
            return model, created
        img = Image.open(file_path)
        kwargs['width'] = img.size[0]
        kwargs['height'] = img.size[1]
        kwargs['img_format'] = img.format
        kwargs['size'] = os.path.getsize(file_path)
        for key, value in kwargs.items():
            setattr(model, key, value)
        return (model, created)


class SearchFile(ImageFile):
    """Search file."""
    __mapper_args__ = {'polymorphic_identity': 'search_file'}
    thumbnail_checksum = db.Column(db.String, db.ForeignKey('image_file.checksum'))
    thumbnail = relationship(
        "ImageFile", backref="thumb_search_files", remote_side='ImageFile.checksum')
    search_url = db.Column(URLType)
    similar_search_url = db.Column(URLType)
    size_search_url = db.Column(URLType)
    image_guess = db.Column(db.String)

    @staticmethod
    def get_page_search_result(file_path):
        """Get page search result from file."""
        res = {
            'image_guess': None,
            'search_url': None,
            'similar_search_url': None,
            'size_search_url': None,
        }
        try:
            res['search_url'] = SearchFile.get_file_post_response(file_path, 'url')
        except Exception as err:  # pylint: disable=broad-except
            log.warning('Error getting search url', err=err)
        if res['search_url'] is not None:
            resp = requests.get(
                res['search_url'], headers={'User-Agent': get_user_agent('firefox')}, timeout=10)
            html_text = resp.text
            keyword_text = 'Our systems have detected unusual traffic from your computer network.'
            if keyword_text in resp.text:
                log.debug('get html with different user agent')
                resp = requests.get(
                    res['search_url'],
                    headers={'User-Agent': get_user_agent('chrome')},
                    timeout=10
                )
                if keyword_text in resp.text:
                    err_msg =  \
                        'Unusual traffic detected, response status code:{}'.format(
                            resp.status_code
                        )
                    log.error(err_msg)
                    raise ValueError(err_msg)
            search_page = BeautifulSoup(html_text, 'lxml')
            base_url = 'https://www.google.com'
            size_search_tag = search_page.select_one('._v6 .gl a')
            if size_search_tag:
                size_search_url = size_search_tag.attrs.get('href', None)
                if size_search_url:
                    res['size_search_url'] = urljoin(base_url, size_search_url)
            similar_search_tag = search_page.select_one('h3._DM a')
            if similar_search_tag:
                similar_search_url = similar_search_tag.attrs.get('href', None)
                if similar_search_url:
                    res['similar_search_url'] = urljoin(base_url, similar_search_url)
            image_guess_tag = search_page.select_one('._hUb a')
            if image_guess_tag:
                res['image_guess'] = image_guess_tag.text
        return res

    @property
    def thumbnail_basename(self):
        """Get thumbnail basename."""
        if self.thumbnail_checksum:
            return self.thumbnail_checksum + '.jpg'

    @property
    def default_thumbnail_path(self):
        """Get default thumbnail path."""
        if self.thumbnail_checksum:
            return os.path.join(THUMB_FOLDER, self.thumbnail_basename)

    def is_thumbnail_exist(self, thumb_folder=THUMB_FOLDER):
        """Check if thumbnail exist."""
        if not self.thumbnail_checksum:
            return
        thumbnail_path = self.get_thumb_path(thumb_folder)
        if not thumbnail_path:
            return None
        return os.path.isfile(thumbnail_path)

    def get_thumb_path(self, thumb_folder=THUMB_FOLDER):
        """Get thumbnail path."""
        if self.thumbnail_checksum:
            return os.path.join(thumb_folder, self.thumbnail_basename)

    def create_thumbnail(self, file_path, thumb_folder=THUMB_FOLDER):
        """Create thumbnail."""
        with tempfile.NamedTemporaryFile() as temp:
            img = Image.open(file_path)
            img.thumbnail((256, 256))
            try:
                img.save(temp.name, 'JPEG')
            except OSError as err:
                log.warning('Error create thumbnail, convert to jpg first', error=err)
                img.convert('RGB').save(temp.name, 'JPEG')
            thumb_checksum = sha256.sha256_checksum(temp.name)
            thumbnail_path = os.path.join(thumb_folder, thumb_checksum + '.jpg')
            if not os.path.isfile(thumbnail_path):
                shutil.copyfile(temp.name, thumbnail_path)
            with db.session.no_autoflush:  # pylint: disable=no-member
                thumb_m, _ = ImageFile.get_or_create_from_file(file_path=thumbnail_path)
                self.thumbnail_checksum = thumb_m.checksum

    @staticmethod
    def get_or_create_from_input_file(
            file_path, thumb_folder=THUMB_FOLDER, get_page_search=False, use_cache=True):
        """Get or create from file."""
        checksum = sha256.sha256_checksum(file_path)
        model, model_created = get_or_create(db.session, SearchFile, checksum=checksum)
        db.session.commit()  # pylint: disable=no-member
        if not model_created and use_cache:
            return model, False
        model.image, _ = ImageFile.get_or_create_from_file(file_path=file_path)
        if not model.is_thumbnail_exist(thumb_folder):
            model.create_thumbnail(file_path, thumb_folder)
        if not get_page_search:
            return model, True
        keys_values = [
            getattr(model, x)
            for x in [
                'image_guess', 'search_url', 'similar_search_url', 'size_search_url']
        ]
        if not any(keys_values) or not use_cache:
            model.cache_page_search_result(file_path)
        return model, True

    def cache_page_search_result(self, file_path):
        """Cache page search result."""
        res = SearchFile.get_page_search_result(file_path)
        for key, item in res.items():
            if item:
                setattr(self, key, item)

    @staticmethod
    def get_file_post_response(file_path, return_mode='response'):
        """Get post response."""
        search_url = 'http://www.google.com/searchbyimage/upload'
        multipart = {'encoded_image': (file_path, open(file_path, 'rb')), 'image_content': ''}
        response = requests.post(search_url, files=multipart, allow_redirects=False)
        if return_mode == 'url':
            return response.headers['Location']
        return response


class SearchModel(db.Model):
    """Search model."""
    TYPES = [
        ('similar', 'Similar'),
        ('size', 'Size'),
    ]
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    search_file_id = db.Column(db.String, db.ForeignKey('image_file.checksum'))
    search_file = relationship(
        "SearchFile", backref="search_model", remote_side='SearchFile.checksum',
        enable_typechecks=False)
    search_file = db.relationship('SearchFile', backref='search_models')
    search_type = db.Column(ChoiceType(TYPES))
    query_url = db.Column(URLType)
    page = db.Column(db.Integer)
    match_results = db.relationship(
        'MatchResult', secondary=search_model_match_results, lazy='subquery',
        backref=db.backref('search_models', lazy=True), enable_typechecks=False)

    @staticmethod
    def get_or_create_from_file(file_input, search_type, page=1, use_cache=True):
        """Get result from file."""
        with db.session.no_autoflush:  # pylint: disable=no-member
            file_model, _ = SearchFile.get_or_create_from_input_file(
                file_input, get_page_search=True, use_cache=use_cache)
        db.session.add(file_model)  # pylint: disable=no-member
        db.session.commit()  # pylint: disable=no-member
        kwargs = {
            'search_file': file_model,
            'search_type': search_type,
            'page': page,
        }
        with db.session.no_autoflush:  # pylint: disable=no-member
            sm_model, created = get_or_create(db.session, SearchModel, **kwargs)
        db.session.add(sm_model)  # pylint: disable=no-member
        db.session.commit()  # pylint: disable=no-member
        if sm_model.match_results and use_cache:
            return sm_model, created
        sm_model.get_match_results()
        return sm_model, created

    def get_match_results(self):
        """Get match results."""
        search_type = self.search_type
        req_url = None
        match_results = []
        if search_type == 'similar':
            req_url = self.search_file.similar_search_url
        elif search_type == 'size':
            req_url = self.search_file.size_search_url
        elif search_type not in list(zip(*SearchModel.TYPES))[0]:
            log.error('Unknown search type', t=search_type)
        else:
            log.debug('Not matching condition', search_type=search_type)
        if req_url is not None:
            resp = requests.get(req_url, headers={'User-Agent': get_user_agent()}, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for html_tag in soup.select('.rg_bx'):
                model, _ = MatchResult.get_or_create_from_html_tag(html_tag)
                match_results.append(model)
        else:
            log.debug('Unknown url', search_type=search_type)
        if match_results:
            self.match_results.extend(match_results)
            db.session.commit()  # pylint: disable=no-member
        return match_results


def get_or_create(session, model, **kwargs):
    """Creates an object or returns the object if exists."""
    instance = session.query(model).filter_by(**kwargs).first()
    created = False
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        created = True
    return instance, created
