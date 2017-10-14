#!/usr/bin/env python3
"""Model module."""
from urllib.parse import parse_qs, urlparse
from datetime import datetime
import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.orm import relationship
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
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    query = db.Column(db.String, nullable=False)
    query_url = db.Column(URLType)
    page = db.Column(db.Integer)
    match_results = db.relationship(
        'MatchResult', secondary=match_results, lazy='subquery',
        backref=db.backref('match_results', lazy=True)
    )
    __table_args__ = (UniqueConstraint('query', 'page'),)


class MatchResult(db.Model):  # pylint: disable=too-few-public-methods
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
    search_query = db.Column(db.Integer, db.ForeignKey('search_query.id'), nullable=False)


class ImageURL(db.Model):  # pylint: disable=too-few-public-methods
    """Image URL."""
    url = db.Column(URLType, primary_key=True)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)


def get_or_create(session, model, **kwargs):
    """Creates an object or returns the object if exists."""
    instance = session.query(model).filter_by(**kwargs).first()
    created = False
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        created = True
    return instance, created
