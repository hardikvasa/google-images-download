"""Test for models module."""
from PIL import Image
from flask import Flask

from google_images_download import models


def test_get_or_create_from_file(tmpdir):
    """Test method."""
    app = Flask(__name__)
    tmp_db = tmpdir.join('temp.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + tmp_db.strpath
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    models.db.init_app(app)
    app.app_context().push()
    models.db.create_all()

    img_input = tmpdir.join("test.jpg")
    thumb_folder = tmpdir.mkdir('thumb')
    img = Image.new('RGB', (500, 500), 'red')
    img.save(img_input.strpath)
    res, created = models.SearchFile.get_or_create_from_input_file(
        img_input.strpath, thumb_folder.strpath)
    assert created
    assert res.image.checksum == \
        '0deee6f6b714650064a6b42b9b306e0a95f12b2e3df54d77c9b8eb2cae78e075'
    assert res.thumbnail.checksum == \
        '9e5ffe7f0af13b394210ff8991eb7d75ade95ba2124a084c9d21fa2234a49428'
    assert res.image.width, res.image.height == (500, 500)
    assert res.thumbnail.width, res.thumbnail.height == (256, 256)
