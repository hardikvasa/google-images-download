#!/usr/bin/env python3
"""Model module."""
from urllib.parse import parse_qs, urlparse
import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.types import URLType, JSONType

db = SQLAlchemy()  # pylint: disable=invalid-name
match_results = db.Table(  # pylint: disable=invalid-name
    'match_results',
    db.Column(
        'match_result_id', db.Integer, db.ForeignKey('match_result.id'),
        primary_key=True
    ),
    db.Column(
        'search_query_id', db.Integer, db.ForeignKey('search_query.id'), primary_key=True)
)


class SearchQuery(db.Model):  # pylint: disable=too-few-public-methods
    """Search query."""
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    query = db.Column(db.String)
    datetime_query = db.Column(db.DateTime, unique=True, nullable=False)
    query_url = db.Column(URLType)
    page = db.Column(db.Integer)
    match_results = db.relationship(
        'MatchResult', secondary=match_results, lazy='subquery',
        backref=db.backref('pages', lazy=True)
    )


class MatchResult(db.Model):  # pylint: disable=too-few-public-methods
    """Match result."""
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    json_data = db.Column(JSONType)
    json_data_id = db.Column(db.String)
    imgres_url = db.Column(URLType)
    data_ved = db.Column(db.String)
    img_url = db.Column(URLType, db.ForeignKey('imageURL.url'), nullable=False)
    search_query = db.Column(
        db.Integer, db.ForeignKey('search_query.id'), nullable=False)

    @property
    def img_url_width(self):
        """Get image url width."""
        return parse_qs(urlparse(self.imgres_url).query).get('w', [None])[0]

    @property
    def img_url_height(self):
        """Get image url height."""
        return parse_qs(urlparse(self.imgres_url).query).get('h', [None])[0]

    @property
    def imgref_url(self):
        """Get image ref url."""
        return parse_qs(urlparse(self.imgres_url).query).get('imgrefurl', [None])[0]

    @property
    def img_url_basename(self):
        """Get image url filename."""
        return os.path.basename(self.img_url)


class ImageURL(db.Model):  # pylint: disable=too-few-public-methods
    """Image URL."""
    url = db.Column(URLType, primary_key=True)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    match_results = db.relationship('MatchResult', backref='image_url', lazy='subquery')


def get_or_create(session, model, **kwargs):
    """Creates an object or returns the object if exists."""
    instance = session.query(model).filter_by(**kwargs).first()
    created = False
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        created = True
    return instance, created
