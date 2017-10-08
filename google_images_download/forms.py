from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class IndexForm(FlaskForm):  # pylint: disable=too-few-public-methods
    """Form for index."""
    query = StringField('query', validators=[DataRequired()])
