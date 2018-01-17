#!/usr/bin/env python3
"""Model module."""
from datetime import datetime
import os

from appdirs import user_data_dir
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP
from sqlalchemy_utils.types import URLType, JSONType, ChoiceType
import structlog


DEFAULT_THUMB_FOLDER = os.path.join(user_data_dir('google_images_download', 'hardikvasa'), 'thumb')  # NOQA
log = structlog.getLogger(__name__)
db = SQLAlchemy()

image_url_tags = db.Table(
    'image_url_tags',
    db.Column('image_url_id', db.Integer, db.ForeignKey('imageURL.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True))
search_image_match_results = db.Table(
    'search_image_match_results',
    db.Column('search_image_page_id', db.Integer, db.ForeignKey('search_image_page.id'), primary_key=True),   # NOQA
    db.Column('match_result_id', db.Integer, db.ForeignKey('match_result.id'), primary_key=True))


class DBVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer, default=1, nullable=False)


class SearchQuery(db.Model):
    """Search query."""
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    search_query = db.Column(db.String, nullable=False)
    page = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        templ = '<SearchQuery:{0.id} query:[{0.search_query}] page:{0.page}>'
        return templ.format(self)


class MatchResult(db.Model):
    """Match result."""
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    imgres_url = db.Column(URLType)
    imgref_url = db.Column(URLType)
    json_data_id = db.Column(db.Integer, db.ForeignKey('json_data.id'))
    json_data = db.relationship(
        'JSONData', lazy='subquery',
        backref=db.backref('match_results', lazy=True))
    search_query_id = db.Column(db.Integer, db.ForeignKey('search_query.id'))
    search_query = db.relationship(
        'SearchQuery', lazy='subquery',
        backref=db.backref('match_results', lazy=True))
    # image and thumbnail
    img_url_id = db.Column(db.Integer, db.ForeignKey('imageURL.id'))
    thumbnail_url_id = db.Column(db.Integer, db.ForeignKey('imageURL.id'))
    img_url = db.relationship(
        'ImageURL', foreign_keys='MatchResult.img_url_id', lazy='subquery',
        backref=db.backref('match_results', lazy=True, cascade='delete'))
    thumbnail_url = relationship(
        'ImageURL', foreign_keys='MatchResult.thumbnail_url_id', lazy='subquery',
        backref=db.backref('thumbnail_match_results', lazy=True, cascade='delete'))


class JSONData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    value = db.Column(JSONType)


class ImageURL(db.Model):
    """Image URL."""
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    url = db.Column(URLType)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    tags = db.relationship(
        'Tag', secondary=image_url_tags, lazy='subquery',
        backref=db.backref('image_urls', lazy=True))

    def __repr__(self):
        templ = '<ImageURL:{0.id} url:{0.url} w:{0.width} h:{0.height}>'
        return templ.format(self)


class Tag(db.Model):
    """Tag model."""
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    namespace = db.Column(db.String)
    name = db.Column(db.String)

    def __repr__(self):
        templ = '<Tag:{0.id} {1}{0.name}>'
        return templ.format(self, '{}:'.format(self.namespace) if self.namespace else '')


class ImageFile(db.Model):
    """Image file model."""
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    checksum = db.Column(db.String)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    img_format = db.Column(db.String)
    size = db.Column(db.Integer)
    thumbnail_id = db.Column(db.Integer, db.ForeignKey('image_file.id'))
    thumbnail = relationship(
        'ImageFile', lazy='subquery', remote_side='ImageFile.id', post_update=True,
        backref=db.backref('original_image_files', lazy=True))


class SearchImage(db.Model):
    """Search image"""
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    img_file_id = db.Column(db.Integer, db.ForeignKey('image_file.id'))
    img_file = relationship(
        'ImageFile', foreign_keys='SearchImage.img_file_id', lazy='subquery',
        backref=db.backref('search_image', lazy=True))
    searched_img_url = db.Column(URLType)
    search_url = db.Column(URLType)
    similar_search_url = db.Column(URLType)
    size_search_url = db.Column(URLType)
    img_guess = db.Column(db.String)


class TextMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    # mostly on every text match obj
    title = db.Column(db.String)
    url = db.Column(URLType)
    url_text = db.Column(db.String)
    text = db.Column(db.String)
    # optional, it also mean there is thumbnail
    imgres_url = db.Column(URLType)
    imgref_url = db.Column(URLType)
    # search image
    search_image_id = db.Column(db.Integer, db.ForeignKey('search_image.id'))
    search_image_model = relationship(
        'SearchImage', foreign_keys='TextMatch.search_image_id', lazy='subquery',
        backref=db.backref('text_matches', lazy=True))
    # image (optional)
    img_url_id = db.Column(db.Integer, db.ForeignKey('imageURL.id'))
    thumbnail_url_id = db.Column(db.Integer, db.ForeignKey('imageURL.id'))
    img_url = db.relationship(
        'ImageURL', foreign_keys='TextMatch.img_url_id', lazy='subquery',
        backref=db.backref('text_matches', lazy=True))
    thumbnail_url = relationship(
        'ImageURL', foreign_keys='TextMatch.thumbnail_url_id', lazy='subquery',
        backref=db.backref('thumbnail_text_matches', lazy=True))


class MainSimilarResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    img_src = db.Column(db.String)
    img_width = db.Column(db.Integer)
    img_height = db.Column(db.Integer)
    img_title = db.Column(db.String)
    search_url = db.Column(URLType)
    search_image_id = db.Column(db.Integer, db.ForeignKey('search_image.id'))
    search_image_model = relationship(
        'SearchImage', foreign_keys='MainSimilarResult.search_image_id', lazy='subquery',
        backref=db.backref('main_similar_results', lazy=True))


class SearchImagePage(db.Model):
    TYPE_SIMILAR = '1'
    TYPE_SIZE = '2'
    TYPES = [
        (TYPE_SIMILAR, 'Similar'),
        (TYPE_SIZE, 'Size'),
    ]
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    page = db.Column(db.Integer, default=1, nullable=False)
    search_type = db.Column(ChoiceType(TYPES))
    search_img_id = db.Column(db.Integer, db.ForeignKey('search_image.id'))
    search_img = relationship(
        'SearchImage', foreign_keys='SearchImagePage.search_img_id', lazy='subquery',
        backref=db.backref('pages', lazy=True))
    match_results = db.relationship(
        'MatchResult', secondary=search_image_match_results, lazy='subquery',
        backref=db.backref('search_image_pages', lazy=True))


def get_or_create(session, model, **kwargs):
    """Creates an object or returns the object if exists."""
    instance = session.query(model).filter_by(**kwargs).first()
    created = False
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        created = True
    return instance, created
