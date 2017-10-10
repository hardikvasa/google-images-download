"""Server module."""
from logging.handlers import TimedRotatingFileHandler
from urllib.parse import urlparse, parse_qs
import datetime
import json
import logging  # pylint: disable=ungrouped-imports
import os

from bs4 import BeautifulSoup
from flask import Flask, render_template
from flask.cli import FlaskGroup
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
import vcr

from google_images_download.forms import IndexForm
from google_images_download import models
from google_images_download.simple_gi import get_json_resp


app = Flask(__name__)  # pylint: disable=invalid-name

logging.basicConfig()
vcr_log = logging.getLogger("vcr")  # pylint: disable=invalid-name
vcr_log.setLevel(logging.INFO)


def get_or_create_search_query(search_query, page, use_cache=True):
    """Get or create search query model."""
    current_datetime = datetime.datetime.now()
    sq_kwargs = {'query': search_query, 'page': page}
    sq_m, sq_created = models.get_or_create(
        models.db.session, models.SearchQuery, **sq_kwargs)
    if sq_created:
        sq_m.datetime_query = current_datetime
        models.db.session.add(sq_m)  # pylint: disable=no-member
        models.db.session.commit()  # pylint: disable=no-member

    else:
        app.logger.debug(
            'Query already created and have %s match',
            len(sq_m.match_results)
        )
    if sq_m.match_results and use_cache:
        return sq_m, sq_created

    match_set = parse_json_resp_for_match_result(
        get_json_resp(search_query, page - 1))

    with models.db.session.no_autoflush:  # pylint: disable=no-member

        for match, imgurl in match_set:
            imgres_url_query = parse_qs(urlparse(match['imgres_url']).query)
            imgurl_kwargs = {
                'url': imgurl,
                'width': imgres_url_query.get('w', [None])[0],
                'height': imgres_url_query.get('h', [None])[0],
            }
            imgurl_m, _ = models.get_or_create(
                models.db.session, models.ImageURL, **imgurl_kwargs)
            match['img_url'] = imgurl_m.url
            match['search_query'] = sq_m.id
            match_in_sq_m = [
                x for x in sq_m.match_results
                if x.json_data_id == match['id']]
            if match_in_sq_m:
                if len(match_in_sq_m) > 1:
                    app.logger.debug(
                        'Found %s match result with same json data',
                        len(match_in_sq_m)
                    )
                assert match_in_sq_m[0].json_data == match['json_data']
                match_m = match_in_sq_m[0]
                # match_m.img_url = match['img_url']
                # match_m.search_query = sq_m.id
            else:
                match_m, _ = models.get_or_create(
                    models.db.session, models.MatchResult, **match)
            sq_m.match_results.append(match_m)
            models.db.session.add(imgurl_m)  # pylint: disable=no-member
            models.db.session.add(match_m)  # pylint: disable=no-member
        models.db.session.add(sq_m)  # pylint: disable=no-member
    models.db.session.commit()  # pylint: disable=no-member
    return sq_m, sq_created


@app.route('/', methods=['GET', 'POST'])
@vcr.use_cassette(record_mode='new_episodes')
def index():
    """Get Index page."""
    form = IndexForm()
    if form.validate_on_submit():
        page = 1
        search_query = form.query.data
        sq_m, _ = get_or_create_search_query(search_query, page - 1)
        app.logger.debug(
            '%s match(s) found for [%s]', len(sq_m.match_results), sq_m.query)
        return render_template('index.html', form=form, entry=sq_m)
    return render_template('index.html', form=form, entry=None)


def parse_json_resp_for_match_result(response):  # pylint: disable=invalid-name
    """Parse json response for match result."""
    soup = BeautifulSoup(response, 'html.parser')
    for match in soup.select('.rg_bx'):
        imgres_url = match.select_one('a').get('href', None)
        json_data = json.loads(match.select_one('.rg_meta').text)
        img_url = parse_qs(urlparse(imgres_url).query)['imgurl'][0]
        match_result = {
            'data_ved': match.get('data-ved', None),
            'json_data': json_data,
            'imgres_url': match.select_one('a').get('href', None),
            'json_data_id': json_data['id']
        }
        yield match_result, img_url


@vcr.use_cassette(record_mode='new_episodes')
def get_example_query_set(query='red'):
    """Get example query set."""
    result = {
        'SearchQuery': {
            'query': query, 'datetime_query': datetime.datetime.now(), 'page': 1
        }
    }
    resp, query_url = get_json_resp(query, return_url=True)
    result['SearchQuery']['query_url'] = query_url
    result['response'] = resp
    soup = BeautifulSoup(resp, 'html.parser')
    result['soup'] = soup
    for match in soup.select('.rg_bx'):
        imgres_url = match.select_one('a').get('href', None)
        json_data = json.loads(match.select_one('.rg_meta').text)
        img_url = parse_qs(urlparse(imgres_url).query)['imgurl'][0]
        match_result = {
            'data_ved': match.get('data-ved', None),
            'json_data': json_data,
            'imgres_url': match.select_one('a').get('href', None),
        }
        result.setdefault('results', []).append(
            {'MatchResult': match_result, 'tag': match, 'ImageURL': img_url})
    return result


def shell_context():
    """Return shell context."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    models.db.init_app(app)
    return {
        'app': app, 'db': models.db, 'models': models,
        'example_query_set': get_example_query_set(),
    }


def create_app(script_info=None):  # pylint: disable=unused-argument
    """Create app."""
    app.shell_context_processor(shell_context)
    try:
        app.config.from_object('google_images_download.server_default_settings')
    except ImportError as err:
        app.logger.debug(
            "Module 'server_default_settings' is not found, error: %s", err)
    try:
        app.config.from_envvar('GOOGLE_IMAGES_DOWNLOAD_SERVER_SETTINGS')
    except RuntimeError as err:
        app.logger.debug(
            "The environment variable "
            "'GOOGLE_IMAGES_DOWNLOAD_SERVER_SETTINGS' is not set, error: %s", err)

    if not app.debug:
        # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
        directory = 'log'
        if not os.path.exists(directory):
            os.makedirs(directory)
        default_log_file = os.path.join(directory, 'google_images_download_server.log')
        file_handler = TimedRotatingFileHandler(
            default_log_file, 'midnight')
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
        app.logger.addHandler(file_handler)

    admin = Admin(app, name='google image download', template_mode='bootstrap3')
    admin.add_view(ModelView(models.SearchQuery, models.db.session))
    admin.add_view(ModelView(models.MatchResult, models.db.session))
    admin.add_view(ModelView(models.ImageURL, models.db.session))
    Bootstrap(app)
    return app


cli = FlaskGroup(create_app=create_app)  # pylint: disable=invalid-name


@app.cli.command()
def debug():
    """Run in debugging mode."""
    app.config.setdefault('WTF_CSRF_ENABLED', False)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gid_debug.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    models.db.init_app(app)
    models.db.create_all()
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)


@app.cli.command()
def initdb():
    """Initialize the database."""
    print('Init the db')


if __name__ == '__main__':
    cli()
