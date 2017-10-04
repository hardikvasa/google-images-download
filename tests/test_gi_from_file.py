"""test module."""
import json
import logging
from urllib.parse import urljoin

import pytest
import vcr


logging.basicConfig(level=logging.DEBUG)
vcr_log = logging.getLogger("vcr")
vcr_log.setLevel(logging.INFO)



@pytest.mark.no_travis
@vcr.use_cassette(record_mode='new_episodes')
def test_search_mode_data():
    """Test search mode data."""
    from google_images_download import gi_from_file as giff
    img_file = '0aee703edbace3306eba90682c43dc37f65722a45d672f17bef2af99c58c47a0.jpg'
    json_file = img_file + '.json'
    with open(json_file) as f:
        json_data = json.load(f)
    res = giff.get_first_page_data(file_path=img_file)
    assert json_data == res


@pytest.mark.no_travis
@vcr.use_cassette(record_mode='new_episodes')
def test_search_mode_largest():
    """Test search mode largest."""
    from google_images_download import gi_from_file as giff
    img_file = '1a1c6e4542cc9bed4d2fbc43300efd5cc291a644170719932343fb78fd34860e.jpg'
    json_file = img_file + '.json'
    session = giff.get_default_session()
    res = giff.get_largest_image(img_file, session)
    with open(json_file) as f:
        json_data = json.load(f)
    assert res == json_data


@pytest.mark.no_travis
@vcr.use_cassette(record_mode='new_episodes')
def test_search_mode_largest_no_match():
    """Test search mode largest."""
    from google_images_download import gi_from_file as giff
    img_file = '3cdaa2a568905f77a4f64db8481a40d90590572c400b186613eacc82e6158284.jpg'
    session = giff.get_default_session()
    res = giff.get_largest_image(img_file, session)
    assert res is None
