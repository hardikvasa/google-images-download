"""Server module."""
from logging.handlers import TimedRotatingFileHandler
import logging

from flask import Flask, render_template
from flask.cli import FlaskGroup

from google_images_download.forms import IndexForm

app = Flask(__name__)  # pylint: disable=invalid-name
# db = SQLAlchemy()  # pylint: disable=invalid-name


@app.route('/', methods=['GET', 'POST'])
def index():
    """Get Index page."""
    form = IndexForm()
    app.logger.warning('sample message')
    if form.validate_on_submit():
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


def shell_context():
    """Return shell context."""
    return {'app': app}


def create_app(script_info=None):  # pylint: disable=unused-argument
    """Create app."""
    # db.init_app(app)
    app.shell_context_processor(shell_context)

    # app.config.from_object('google_images_download.server_default_settings')
    try:
        app.config.from_envvar('GOOGLE_IMAGES_DOWNLOAD_SERVER_SETTINGS')
    except RuntimeError:
        app.logger.debug(
            "The environment variable "
            "'GOOGLE_IMAGES_DOWNLOAD_SERVER_SETTINGS' is not set")

    if not app.debug:
        # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
        default_log_file = 'google_images_download_server.log'
        # file_handler = TimedRotatingFileHandler(
        # os.path.join(app.config['LOG_DIR'], 'candidtim_flask.log'), 'midnight')
        file_handler = TimedRotatingFileHandler(default_log_file, 'midnight')
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
        app.logger.addHandler(file_handler)

    # admin = Admin(app, name='microblog', template_mode='bootstrap3')
    # Add administrative views here
    return app


cli = FlaskGroup(create_app=create_app)  # pylint: disable=invalid-name


@app.cli.command()
def debug():
    """Run in debugging mode."""
    app.config.setdefault('WTF_CSRF_ENABLED', False)
    app.run(debug=True)


@app.cli.command()
def initdb():
    """Initialize the database."""
    print('Init the db')


if __name__ == '__main__':
    cli()
