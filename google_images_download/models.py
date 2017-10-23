#!/usr/bin/env python3
"""Model module."""
from urllib.parse import urlparse
from datetime import datetime
import os
import tempfile
import shutil

from appdirs import user_data_dir
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP
from sqlalchemy_utils.types import URLType, JSONType, ChoiceType

from google_images_download import sha256

db = SQLAlchemy()  # pylint: disable=invalid-name
match_results = db.Table(  # pylint: disable=invalid-name
    'match_results',
    db.Column(
        'match_result_id', db.Integer, db.ForeignKey('match_result.id'), primary_key=True),
    db.Column('search_query_id', db.Integer, db.ForeignKey('search_query.id'), primary_key=True))
match_result_tags = db.Table(  # pylint: disable=invalid-name
    'match_result_tags',
    db.Column('match_result_id', db.Integer, db.ForeignKey('match_result.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.full_name'), primary_key=True))
search_query_tags = db.Table(  # pylint: disable=invalid-name
    'search_query_tags',
    db.Column('search_query_id', db.Integer, db.ForeignKey('search_query.id'), primary_key=True),
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
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    query = db.Column(db.String, nullable=False)
    query_url = db.Column(URLType)
    page = db.Column(db.Integer)
    match_results = db.relationship(
        'MatchResult', secondary=match_results, lazy='subquery',
        backref=db.backref('search_query', lazy=True))
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
    def get_or_create_from_input_file(file_path, thumb_folder=THUMB_FOLDER):
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
        return model, True


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
