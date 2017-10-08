"""Server module."""
from urllib.parse import urlencode
from logging.handlers import TimedRotatingFileHandler
import datetime
import logging  # pylint: disable=ungrouped-imports
import os

from fake_useragent import UserAgent
from flask import Flask, render_template
from flask.cli import FlaskGroup
import requests
import vcr

from google_images_download.forms import IndexForm

app = Flask(__name__)  # pylint: disable=invalid-name
# db = SQLAlchemy()  # pylint: disable=invalid-name
logging.basicConfig()
vcr_log = logging.getLogger("vcr")
vcr_log.setLevel(logging.INFO)


@app.route('/', methods=['GET', 'POST'])
@vcr.use_cassette(record_mode='new_episodes')
def index():
    """Get Index page."""
    form = IndexForm()
    if form.validate_on_submit():
        query = form.query.data
        url_base = 'https://google.com/search?{}'
        url_q_dict = {'q': query, 'tbm': 'isch'}
        url_q = url_base.format(urlencode(url_q_dict))
        q_datetime_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dump_html = os.path.join('dump', q_datetime_str + '.html')

        ua = UserAgent()
        resp = requests.get(
            url_q, timeout=10, headers={'User-Agent': ua.firefox})
        try:
            with open(dump_html, 'w') as f:
                f.write(resp.text)
        except OSError:
            app.logger.debug('OS error when dumping resp text.')
            dump_html_dir = os.path.dirname(dump_html)
            if not os.path.exists(dump_html_dir):
                os.makedirs(dump_html_dir)
            with open(dump_html, 'w+') as f:
                f.write(resp.text)

        debug_info = {}
        if app.debug:
            debug_info['query'] = query
            debug_info['url'] = url_q
            debug_info['dump_html'] = (
                os.path.abspath(dump_html), q_datetime_str + '.html')
        return render_template(
            'index.html', form=form, query=query, debug_info=debug_info)
    app.logger.warning('sample message2')
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
        file_handler = TimedRotatingFileHandler(
            default_log_file, 'midnight')
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
