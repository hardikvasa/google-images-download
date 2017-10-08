"""Server module."""
from urllib.parse import urlencode
from logging.handlers import TimedRotatingFileHandler
import datetime
import json
import logging  # pylint: disable=ungrouped-imports
import os

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from flask import Flask, render_template
from flask.cli import FlaskGroup
from flask_bootstrap import Bootstrap
import requests
import vcr

from google_images_download.forms import IndexForm

app = Flask(__name__)  # pylint: disable=invalid-name
# db = SQLAlchemy()  # pylint: disable=invalid-name
logging.basicConfig()
vcr_log = logging.getLogger("vcr")
vcr_log.setLevel(logging.INFO)


def dump_html(response, html_path):
    """Dump html from requests.get response."""
    try:
        with open(html_path, 'w') as f:
            f.write(response.text)
    except OSError:
        app.logger.debug('OS error when dumping resp text.')
        dump_html_dir = os.path.dirname(html_path)
        if not os.path.exists(dump_html_dir):
            os.makedirs(dump_html_dir)
        with open(html_path, 'w+') as f:
            f.write(response.text)


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
        dump_html_path = os.path.join('dump', q_datetime_str + '.html')

        ua = UserAgent()
        resp = requests.get(
            url_q, timeout=10, headers={'User-Agent': ua.firefox})
        soup = BeautifulSoup(resp.text, 'html.parser')
        result = {'match': []}
        match_tags = []
        match_tags.extend(soup.select('#rg_s div.rg_bx'))
        match_tags.extend(soup.select('.rg_add_chunk div.rg_bx'))
        ou_values = []
        for match_tag in match_tags:
            rg_meta_tag = match_tag.select_one('.rg_meta')
            if rg_meta_tag:
                json_data = json.loads(rg_meta_tag.text),
                result['match'].append({'json_data': json_data})
                ou_values.append(json_data[0]['ou'])
        app.logger.debug(
            '%s match(s) found for [%s]', len(result['match']), query)

        debug_info = {}
        if app.debug:
            dump_html(resp, dump_html_path)
            debug_info['query'] = query
            debug_info['url'] = url_q
            debug_info['dump_html'] = (
                os.path.abspath(dump_html_path), q_datetime_str + '.html')
        return render_template(
            'index.html', form=form, query=query, debug_info=debug_info, result=result)
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
    Bootstrap(app)
    return app


cli = FlaskGroup(create_app=create_app)  # pylint: disable=invalid-name


@app.cli.command()
def debug():
    """Run in debugging mode."""
    app.config.setdefault('WTF_CSRF_ENABLED', False)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)


@app.cli.command()
def initdb():
    """Initialize the database."""
    print('Init the db')


if __name__ == '__main__':
    cli()
