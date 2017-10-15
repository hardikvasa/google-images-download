#!/usr/bin/env python3
"""Model module."""
from urllib.parse import urlparse
from datetime import datetime
import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import URLType, JSONType

db = SQLAlchemy()  # pylint: disable=invalid-name
match_results = db.Table(  # pylint: disable=invalid-name
    'match_results',
    db.Column(
        'match_result_id', db.Integer, db.ForeignKey('match_result.id'), primary_key=True),
    db.Column('search_query_id', db.Integer, db.ForeignKey('search_query.id'), primary_key=True))
match_result_tags = db.Table(  # pylint: disable=invalid-name
    'match_result_tags',
    db.Column('match_result_id', db.Integer, db.ForeignKey('match_result.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True))
search_query_tags = db.Table(  # pylint: disable=invalid-name
    'search_query_tags',
    db.Column('search_query_id', db.Integer, db.ForeignKey('search_query.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True))
image_url_tags = db.Table(  # pylint: disable=invalid-name
    'image_url_tags',
    db.Column('image_url_id', db.Integer, db.ForeignKey('imageURL.url'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True))


class SearchQuery(db.Model):
    """Search query."""
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    query = db.Column(db.String, nullable=False)
    query_url = db.Column(URLType)
    page = db.Column(db.Integer)
    match_results = db.relationship(
        'MatchResult', secondary=match_results, lazy='subquery',
        backref=db.backref('match_results', lazy=True))
    tags = db.relationship(
        'Tag', secondary=search_query_tags, lazy='subquery',
        backref=db.backref('search_query', lazy=True))

    def __repr__(self):
        """Repr."""
        return '<Search query {}, query:[{}] page: {}>'.format(self.id, self.query, self.page)


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
    search_query = db.Column(db.Integer, db.ForeignKey('search_query.id'), nullable=False)
    tags = db.relationship(
        'Tag', secondary=match_result_tags, lazy='subquery',
        backref=db.backref('match_results', lazy=True))

    def __repr__(self):
        """Repr."""
        return '<Match result {}, site: {}, title: {}>'.format(
            self.id, self.site, self.picture_title)


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
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    name = db.Column(db.String, nullable=False)
    namespace = db.Column(db.String)

    def __repr__(self):
        """Repr."""
        return '<Tag {}, {}>'.format(self.id, self.full_name)

    @property
    def full_name(self):
        """Get tag full name format."""
        if self.namespace:
            return '{}:{}'.format(self.namespace, self.name)
        return self.name


def get_or_create(session, model, **kwargs):
    """Creates an object or returns the object if exists."""
    instance = session.query(model).filter_by(**kwargs).first()
    created = False
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        created = True
    return instance, created
