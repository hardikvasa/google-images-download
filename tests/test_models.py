"""Test for models module."""
from urllib.parse import urlparse, parse_qs
import os

from PIL import Image
import pytest
import vcr

from google_images_download import models


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
        'image_guess': 'check for dead pixels',
        'search_url':
            'http://www.google.com/search?'
            'tbs=sbi:AMhZZivJeVMaIy-Czt346tQLdTKhmNlzyMCacQBuRdR3KsVoGDZl7bwKFXeTOX8aRP8_1rrffzyqe'
            'vAHM-ZLF66B4dawe_1IgVqNQgJokBnCO8-hSrXOLBJfT1dCB4uTj1A3wa-z8qKvyhRVN2txG_1BtlXYUmtHOF'
            'z8Te9iHANJk-_1f44BXXWI9Zbq9Yd-JOgXPmaIjzT6FHT4UFGJ2S69P1ixik_1pTLhXQp0Yp0V2aGhs396O93'
            'tCrTnkIpqroTlyVHd5h_1iX6FfD0Vcw60Z9DLnPXOFLAyLmB-HILSFgYxH72V5GjCxDDv4GGwhG-8tV6n4dmk'
            'CgGVhs',
        'similar_search_url':
            'https://www.google.com/search?'
            'tbs=simg:CAEShgIJAGUUt_1bm7g0a-gELEKjU2AQaBAgVCAgMCxCwjKcIGl8KXQgDEiVH_1wi0As8B_1ggos'
            'gLyAvgIKaArsyqIJ9conTehK4QjnjesNtMnGjDr2WYL3JwKke7gjGUtkou0VlOLR40JczbbhOx4-RDy03I_1k'
            'UV6WgCRiPqIUovom1AgBAwLEI6u_1ggaCgoICAESBM9Xj5QMCxCd7cEJGmkKGAoGb3Jhbmdl2qWI9gMKCggvb'
            'S8wamNfcAoYCgVwZWFjaNqliPYDCwoJL20vMDNyMTh5ChkKB3BhdHRlcm7apYj2AwoKCC9tLzBod2t5ChgKBW'
            'FtYmVy2qWI9gMLCgkvbS8wNGQwMWYM&'
            'q=check+for+dead+pixels&tbm=isch&sa=X&ved=0ahUKEwi3o6zp3IrXAhUJahoKHfAKCekQsw4INQ',
        'size_search_url':
            'https://www.google.com/search?'
            'q=check+for+dead+pixels&'
            'tbm=isch&tbs=simg:CAQSlAEJAGUUt_1bm7g0aiAELEKjU2AQaBAgVCAgMCxCwjKcIGl8KXQgDEiVH_1wi0A'
            's8B_1ggosgLyAvgIKaArsyqIJ9conTehK4QjnjesNtMnGjDr2WYL3JwKke7gjGUtkou0VlOLR40JczbbhOx4-'
            'RDy03I_1kUV6WgCRiPqIUovom1AgBAwLEI6u_1ggaCgoICAESBM9Xj5QM&sa=X&'
            'ved=0ahUKEwi3o6zp3IrXAhUJahoKHfAKCekQ2A4IIygB'}


@pytest.mark.no_travis
@vcr.use_cassette('cassette/test_get_page_search_result.yaml', record_mode='new_episodes')
def test_get_page_search_result(tmp_pic):  # pylint: disable=redefined-outer-name
    """test method."""
    res = models.SearchFile.get_page_search_result(tmp_pic['image_input'].strpath)
    for key in ['search_url', 'similar_search_url', 'size_search_url', 'image_guess']:
        assert res[key] == tmp_pic[key], 'error on key: {}'.format(key)


@pytest.mark.no_travis
def test_get_or_create_from_query(tmp_db):
    # pylint: disable=redefined-outer-name, unused-argument
    """Test method."""
    query = 'red'
    query_url = \
        'https://www.google.com/search' \
        '?ijn=1&async=_id%3Arg_s%2C_pms%3As&q=red&tbm=isch&start=100&asearch=ichunk'
    model1, created = models.SearchQuery.get_or_create_from_query(query)
    assert created
    exp_vars1 = {'page': 1, 'query': query, 'query_url': query_url}

    def assert_model_and_exp_vars(model, exp_vars):
        """Assert model and exp vars."""
        model_vars = vars(model)
        for key, item in exp_vars.items():
            if key == 'query_url':
                model_url = urlparse(model_vars[key])
                ev_url = urlparse(exp_vars[key])
                urlparse_keys = ['scheme', 'netloc', 'path', 'params', 'query', 'fragment']
                for ukey in urlparse_keys:
                    if ukey == 'query':
                        assert \
                            parse_qs(getattr(model_url, ukey)) == parse_qs(getattr(ev_url, ukey))
                    else:
                        assert getattr(model_url, ukey) == getattr(ev_url, ukey)
            else:
                assert item == model_vars[key]

    assert_model_and_exp_vars(model1, exp_vars1)

    model2, created = models.SearchQuery.get_or_create_from_query(query)
    assert not created
    assert_model_and_exp_vars(model2, exp_vars1)


@pytest.mark.no_travis
@vcr.use_cassette('cassette/test_get_match_results.yaml', record_mode='new_episodes')
def test_get_match_results(tmp_db):
    # pylint: disable=redefined-outer-name, unused-argument
    """Test method."""
    search_query, _ = models.SearchQuery.get_or_create_from_query('red')
    res = search_query.get_match_results()
    item = res[0]
    assert item.thumbnail
    assert item.thumbnail.height > 0
    assert item.thumbnail.width > 0
    assert item.image
    assert item.image.height > 0
    assert item.image.width > 0


@pytest.mark.no_travis
@vcr.use_cassette('cassette/test_unique_result_on_multisearch.yaml', record_mode='new_episodes')
def test_unique_result_on_multisearch(tmp_db):
    # pylint: disable=unused-argument,redefined-outer-name,invalid-name
    """Test method."""
    model, _ = models.SearchQuery.get_or_create_from_query('red')
    model.get_match_results()
    model, _ = models.SearchQuery.get_or_create_from_query('red', page=2)
    model.get_match_results()
    m_res = models.MatchResult.query.all()
    assert len(m_res) == 200


@pytest.mark.no_travis
@vcr.use_cassette('cassette/test_get_or_create_from_google_url.yaml', record_mode='new_episodes')
def test_get_or_create_from_google_url(tmp_db):
    # pylint: disable=unused-argument,redefined-outer-name,invalid-name
    """Test method."""
    url = \
        'https://www.google.co.id/search?biw=1362&bih=576&tbm=isch&sa=1'\
        '&q=kobayashi+maid&oq=kobayashi+maid' \
        '&gs_l=psy-ab.3..0j0i67k1l3j0j0i67k1j0l2j0i67k1j0.10744.' \
        '12509.0.12676.7.6.1.0.0.0.334.474.0j1j0j1.2.0....0...1.1.64.' \
        'psy-ab..4.3.482....0.HOUo_YnMT8k#imgrc=_'
    model, _ = models.GoogleURLQuery.get_or_create_from_google_url(url)
    res = model.get_match_results()
    assert len(res) > 0  # pylint: disable=len-as-condition


@pytest.mark.no_travis
@vcr.use_cassette('cassette/test_get_result_from_file.yaml', record_mode='new_episodes')
def test_get_result_from_file(tmp_db, tmp_pic):
    # pylint: disable=unused-argument,redefined-outer-name,invalid-name
    """Test method."""
    os.makedirs(models.THUMB_FOLDER, exist_ok=True)
    model, created = models.SearchModel.get_or_create_from_file(
        tmp_pic['image_input'].strpath, 'size')
    first_match_result_total = len(model.match_results)
    url_keys = ['search_url', 'similar_search_url', 'size_search_url', 'image_guess']
    for key in url_keys:
        assert getattr(model.search_file, key), 'key:{}'.format(key)
    assert created
    assert first_match_result_total > 0  # pylint: disable=len-as-condition
    assert model.search_file_id == tmp_pic['checksum']
    assert model.search_file.thumbnail_checksum == tmp_pic['thumb_checksum']
    model, created = models.SearchModel.get_or_create_from_file(
        tmp_pic['image_input'].strpath, 'size')
    assert not created
    assert first_match_result_total == len(model.match_results)
