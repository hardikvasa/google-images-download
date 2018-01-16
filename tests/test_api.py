"""Test for api module."""
import pytest
import requests
import vcr
from PIL import Image

from google_images_download import api, models


@pytest.fixture()
def tmp_pic(tmpdir):
    """Temporary pic."""
    img_input = tmpdir.join("test.jpg")
    img = Image.new('RGB', (500, 500), 'red')
    img.save(img_input.strpath)
    return {
        'image_input': img_input,
        'image': img,
        'checksum': '0deee6f6b714650064a6b42b9b306e0a95f12b2e3df54d77c9b8eb2cae78e075',
        'thumb_checksum': '9e5ffe7f0af13b394210ff8991eb7d75ade95ba2124a084c9d21fa2234a49428',
        'image_size': (500, 500),
        'thumb_size': (250, 250),
    }


@pytest.mark.no_travis
@vcr.use_cassette('cassette/test_get_or_create_search_query.yaml', record_mode='new_episodes')
def test_get_or_create_search_query(tmp_db):
    """test method."""
    res = api.get_or_create_search_query('red picture')[0]
    assert res
    assert all([x.img_url for x in res.match_results])


@pytest.mark.no_travis
@vcr.use_cassette('cassette/test_get_or_create_search_query_duplicate.yaml', record_mode='new_episodes')  # NOQA
def test_get_or_create_search_query_duplicate(tmp_db):
    """test method."""
    v1 = api.get_or_create_search_query('red picture', disable_cache=True)[0]
    v2 = api.get_or_create_search_query('red picture', disable_cache=True)[0]
    tmp_db.session.add_all([v1, v2])
    tmp_db.session.commit()
    assert models.MatchResult.query.count() == 100


@pytest.mark.no_travis
@vcr.use_cassette('cassette/test_get_or_create_match_result_from_json_resp.yaml', record_mode='new_episodes')  # NOQA
def test_get_or_create_match_result_from_json_resp(tmp_db):
    """test method."""
    query_url = \
        'https://www.google.com/search' \
        '?q=red+picture&tbm=isch&ijn=0&start=0&asearch=ichunk&async=_id%3Arg_s%2C_pms%3As'
    resp = requests.get(query_url)
    json_resp = resp.json()
    res = api.get_or_create_match_result_from_json_resp(json_resp)
    m1 = next(res)
    assert m1[1]
    assert m1[0].img_url
    tmp_db.session.add(m1[0])
    tmp_db.session.commit()
    assert m1[0].img_url
    m_list = [m1[0]]
    m_list.extend([x[0] for x in res])
    assert all([x.img_url for x in m_list])


def test_add_tags_to_image_url(tmp_db):
    """test method."""
    args = {
        'img_url': {'url': 'http://example.com/1.jpg', 'width': 2560, 'height': 1920},
        'img_url_tags': [
            {'name': 'picture title', 'namespace': 'picture title'},
            {'name': 'site', 'namespace': 'site'},
            {'name': 'site', 'namespace': 'site'},
            {'name': 'img', 'namespace': 'img ext'}],
    }
    img_url, _ = models.get_or_create(
        tmp_db.session, models.ImageURL, **args['img_url'])
    img_url_tags = api.add_tags_to_image_url(img_url, args['img_url_tags'])
    models.db.session.add_all([img_url] + img_url_tags)
    models.db.session.commit()
    assert len(img_url.tags) > 0


@pytest.mark.no_travis
@vcr.use_cassette('cassette/test_get_or_create_search_image.yaml', record_mode='new_episodes')  # NOQA
def test_get_or_create_search_image(tmp_pic, tmp_db, tmpdir):
    """test method."""
    res, created = api.get_or_create_search_image(
        tmp_pic['image_input'].strpath, thumb_folder=tmpdir.strpath)
    assert created
    assert len(res.text_matches) > 2
    assert len(res.main_similar_results) > 2
