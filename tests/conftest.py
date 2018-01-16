"""Module contain shared fixture function."""
from flask import Flask
import pytest
import structlog

from google_images_download import models


log = structlog.getLogger(__name__)


@pytest.fixture()
def tmp_db(tmpdir):
    """Get tmp db."""
    app = Flask(__name__)
    tmp_db_path = tmpdir.join('temp.db')
    log.debug('db path', v=tmp_db_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + tmp_db_path.strpath
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    models.db.init_app(app)
    app.app_context().push()
    models.db.create_all()
    return models.db
