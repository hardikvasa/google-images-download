"""Forms module."""
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional, ValidationError


def validate_postitive_number(_, field):
    """Check limit."""
    if not field.data > 0:
        raise ValidationError('Limit must be bigger than 0')


class IndexForm(FlaskForm):  # pylint: disable=too-few-public-methods
    """Form for index."""
    query = StringField('query', validators=[DataRequired()])
    disable_image = BooleanField(validators=[Optional()])
    limit = IntegerField(validators=[Optional(), validate_postitive_number])
    page = IntegerField(validators=[Optional(), validate_postitive_number])


class FileForm(FlaskForm):
    """Form for getting result from file search."""
    file_path = StringField('File Path', validators=[DataRequired()])
    search_type = SelectField(
        'Search Type', validators=[Optional()], choices=[('similar', 'similar'), ('size', 'size')])
    disable_image = BooleanField(validators=[Optional()])
    disable_cache = BooleanField(validators=[Optional()])
