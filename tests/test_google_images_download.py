"""test"""


def test_rename_basename():
    """test."""
    from google_images_download.google_images_download import rename_basename
    assert '/home/user/Downloads/dog.jpg' == \
        rename_basename('/home/user/Downloads/cat.jpg', 'dog')
