"""Forms module."""
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField
from wtforms.validators import DataRequired, Optional


from google_images_download import models


class IndexForm(FlaskForm):  # pylint: disable=too-few-public-methods
    """Form for index."""
    query = StringField('query', validators=[DataRequired()])
    disable_cache = BooleanField(validators=[Optional()])


class FindImageForm(FlaskForm):
    """Form for getting result from file search."""
    file_path = StringField('File Path', validators=[Optional()])
    url = StringField('URL', validators=[Optional()])
    search_type = SelectField('Search Type', validators=[Optional()], choices=models.SearchImagePage.TYPES)  # NOQA
    disable_cache = BooleanField(validators=[Optional()])
