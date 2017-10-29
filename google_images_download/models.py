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
from fake_useragent import UserAgent
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP
from sqlalchemy_utils.types import URLType, JSONType, ChoiceType
import requests
import structlog

from google_images_download import sha256


log = structlog.getLogger(__name__)   # pylint: disable=invalid-name

db = SQLAlchemy()  # pylint: disable=invalid-name
match_results = db.Table(  # pylint: disable=invalid-name
    'match_results',
    db.Column(
        'match_result_id', db.Integer, db.ForeignKey('match_result.id'), primary_key=True),
    db.Column('search_query_url', db.Integer, db.ForeignKey('search_query.query_url'), primary_key=True))
match_result_tags = db.Table(  # pylint: disable=invalid-name
    'match_result_tags',
    db.Column('match_result_id', db.Integer, db.ForeignKey('match_result.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.full_name'), primary_key=True))
search_query_tags = db.Table(  # pylint: disable=invalid-name
    'search_query_tags',
    db.Column('search_query_url', db.Integer, db.ForeignKey('search_query.query_url'), primary_key=True),
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


class SearchQuery(db.Model):
    """Search query."""
    query_url = db.Column(URLType, primary_key=True)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    query = db.Column(db.String, nullable=False)
    page = db.Column(db.Integer)
    match_results = db.relationship(
        'MatchResult', secondary=match_results, lazy='subquery',
        backref=db.backref('search_query', lazy=True))
    tags = db.relationship(
        'Tag', secondary=search_query_tags, lazy='subquery',
        backref=db.backref('search_query', lazy=True))

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
        res = MatchResult.get_or_create_from_json_resp(resp.json())
        match_results = [x[0] for x in res]
        self.match_results.add(match_results)
        return match_results


class MatchResult(db.Model):
    """Match result."""
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    data_ved = db.Column(db.String)
    imgres_url = db.Column(URLType)
    imgref_url = db.Column(URLType)
    # column with valuew from json data
    json_data = db.Column(JSONType)
    json_data_id = db.Column(db.String)
    picture_title = db.Column(db.String)
    site = db.Column(URLType)
    site_title = db.Column(db.String)
    img_ext = db.Column(db.String)
    json_search_url = db.Column(db.String)
    # image and thumbnail
    img_url = db.Column(URLType, db.ForeignKey('imageURL.url'), nullable=False)
    thumb_url = db.Column(URLType, db.ForeignKey('imageURL.url'), nullable=False)
    image = db.relationship('ImageURL', foreign_keys='MatchResult.img_url')
    thumbnail = relationship('ImageURL', foreign_keys='MatchResult.thumb_url')
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
        if json_data['msu'] != json_data['si']:
            log.warning(
                ''.join(ndiff([json_data['msu']], [json_data['si']])))
        kwargs = {
            'data_ved': html_tag.get('data-ved', None),
            'imgres_url': imgres_url,
            'imgref_url': imgref_url,
            # json data
            'json_data': json_data,
            'json_data_id': json_data['id'],
            'picture_title': json_data['pt'],
            'site': json_data['isu'],
            'site_title': json_data.get('st', None),
            'img_ext': json_data['ity'],
            'json_search_url': urljoin('https://www.google.com', json_data['msu'])
        }
        return get_or_create(db.session, MatchResult, **kwargs)


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
        kwargs = {'checksum': sha256.sha256_checksum(file_path)}
        img = Image.open(file_path)
        kwargs['width'] = img.size[0]
        kwargs['height'] = img.size[1]
        kwargs['img_format'] = img.format
        kwargs['size'] = os.path.getsize(file_path)
        model, created = get_or_create(
            db.session, ImageFile, **kwargs)
        if not created:
            return model, False
        return model, True


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

    def get_thumb_path(self, thumb_folder=THUMB_FOLDER):
        """Get thumbnail path."""
        if self.thumbnail_checksum:
            return os.path.join(thumb_folder, self.thumbnail_checksum + '.jpg')

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
            user_agent = UserAgent()
            resp = requests.get(res['search_url'], headers={'User-Agent': user_agent.firefox})
            search_page = BeautifulSoup(resp.text, 'lxml')
            base_url = 'https://www.google.com'
            size_search_url = search_page.select_one('._v6 .gl a').attrs.get('href', None)
            if size_search_url:
                res['size_search_url'] = urljoin(base_url, size_search_url)
            similar_search_url = search_page.select_one('h3._DM a').attrs.get('href', None)
            if similar_search_url:
                res['similar_search_url'] = urljoin(base_url, similar_search_url)
            res['image_guess'] = search_page.select_one('._hUb a').text
        return res

    @staticmethod
    def get_or_create_from_input_file(file_path, thumb_folder=THUMB_FOLDER, get_page_search=False):
        """Get or create from file."""
        checksum = sha256.sha256_checksum(file_path)
        model, model_created = get_or_create(db.session, SearchFile, checksum=checksum)
        if not model_created:
            return model, False
        model.image = ImageFile.get_or_create_from_file(file_path=file_path)[0]
        with tempfile.NamedTemporaryFile() as temp:
            img = Image.open(file_path)
            img.thumbnail((256, 256))
            img.save(temp.name, 'JPEG')
            thumb_checksum = sha256.sha256_checksum(temp.name)
            model.checksum = thumb_checksum
            thumbnail_path = os.path.join(thumb_folder, thumb_checksum + '.jpg')
            if not os.path.isfile(thumbnail_path):
                shutil.copyfile(temp.name, thumbnail_path)
            with db.session.no_autoflush:  # pylint: disable=no-member
                thumb_m, _ = ImageFile.get_or_create_from_file(file_path=thumbnail_path)
                model.thumbnail = thumb_m
        if not get_page_search:
            return model, True
        res = model.SearchFile.get_page_search_result(file_path)
        for key, item in res.items():
            if item:
                setattr(model, key, item)
        return model, True

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
    search_file_id = db.ForeignKey('search_file.checksum')
    search_type = db.Column(ChoiceType(TYPES))
    page = db.Column(db.Integer)
    match_results = db.relationship(
        'MatchResult', secondary=search_model_match_results, lazy='subquery',
        backref=db.backref('search_models', lazy=True))


def get_or_create(session, model, **kwargs):
    """Creates an object or returns the object if exists."""
    instance = session.query(model).filter_by(**kwargs).first()
    created = False
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        created = True
    return instance, created
