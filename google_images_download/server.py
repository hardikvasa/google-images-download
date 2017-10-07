"""Server module."""
from logging.handlers import TimedRotatingFileHandler
import logging
# import os

from flask import Flask, render_template
from flask.cli import FlaskGroup

app = Flask(__name__)  # pylint: disable=invalid-name
# db = SQLAlchemy()  # pylint: disable=invalid-name


@app.route('/')
def index():
    """Get Index page."""
    app.logger.warning('sample message')
    return render_template('index.html')


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


@app.cli.command
def custom_command():
    """Run custom command."""
    print('custom_command run')


@app.cli.command()
def initdb():
    """Initialize the database."""
    print('Init the db')


if __name__ == '__main__':
    cli()
