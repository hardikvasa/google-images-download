"""Test server."""
import logging
import os
import tempfile
import unittest

import pytest
import vcr

from google_images_download import server
from google_images_download import models


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)  # pylint: disable=invalid-name
vcr_log = logging.getLogger("vcr")  # pylint: disable=invalid-name
vcr_log.setLevel(logging.INFO)


class ServerTestCase(unittest.TestCase):
    """Server test case."""

    def setUp(self):
        self.db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
        server.app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:///:memory:'
        server.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = \
            False
        server.app.testing = True
        self.client = server.app.test_client()
        # setting app config to suppres warning
        with server.app.app_context():
            self.client.application.config.setdefault('WTF_CSRF_ENABLED', False)
            models.db.init_app(self.client.application)
            models.db.create_all()
            try:
                server.Bootstrap(self.client.application)
            except AssertionError as err:
                log.debug('Expected error: %s', err)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(server.app.config['DATABASE'])

    def test_index(self):
        """Test index."""
        retval = self.client.get('/')
        assert retval.status_code == 200
        assert retval.data.decode()

    @pytest.mark.no_travis
    @vcr.use_cassette(record_mode='new_episodes')
    def test_query(self):
        """Test method."""
        with self.client.application.app_context():
            sq_m, sq_m_created = server.get_or_create_search_query('red', 1)
            assert sq_m
            assert sq_m_created
            sq_m, sq_m_created = server.get_or_create_search_query('red', 1)
            assert len(sq_m.match_results) == 100
            assert not sq_m_created
            sq_m, sq_m_created = server.get_or_create_search_query(
                'red', 1, use_cache=False)
            assert len(sq_m.match_results) == 100
            assert not sq_m_created


if __name__ == '__main__':
    unittest.main()
