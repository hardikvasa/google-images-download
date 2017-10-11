from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Optional, ValidationError


def validate_limit(_, field):
    """Check limit."""
    if not field.data > 0:
        raise ValidationError('Limit must be bigger than 0')


class IndexForm(FlaskForm):  # pylint: disable=too-few-public-methods
    """Form for index."""
    query = StringField('query', validators=[DataRequired()])
    disable_image = BooleanField(validators=[Optional()])
    limit = IntegerField(validators=[Optional(), validate_limit])
