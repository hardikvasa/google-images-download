"""test module."""
import json
import logging

import pytest
import vcr


logging.basicConfig()
vcr_log = logging.getLogger("vcr")
vcr_log.setLevel(logging.INFO)



@pytest.mark.no_travis
@vcr.use_cassette(record_mode='new_episodes')
def test_search_mode_data():
    """Test search mode data."""
    from google_images_download import gi_from_file as giff
    img_file = '0aee703edbace3306eba90682c43dc37f65722a45d672f17bef2af99c58' \
        'c47a0.jpg'
    json_file = img_file + '.json'
    with open(json_file) as f:
        json_data = json.load(f)
    res = giff.get_first_page_data(file_path=img_file)
    assert json_data == res
