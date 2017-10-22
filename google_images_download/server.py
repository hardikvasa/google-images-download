"""Server module."""
from difflib import ndiff
from logging.handlers import TimedRotatingFileHandler
from urllib.parse import urlparse, parse_qs, urlencode, urljoin
from json.decoder import JSONDecodeError
import datetime
import json
import logging  # pylint: disable=ungrouped-imports
import os

from bs4 import BeautifulSoup
from flask import Flask, render_template, request, url_for, flash
from flask_restless import APIManager  # pylint: disable=import-error
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
import click
import vcr

from google_images_download.forms import IndexForm
from google_images_download import models, pagination, admin
from google_images_download.simple_gi import get_json_resp, get_json_resp_query_url


app = Flask(__name__)  # pylint: disable=invalid-name

vcr_log = logging.getLogger("vcr")  # pylint: disable=invalid-name
vcr_log.setLevel(logging.INFO)


def cache_search_query(search_query_model):
    """Cache search query."""
    # compatibility
    sq_m = search_query_model
    page = sq_m.page

    try:
        matches = parse_json_resp_for_match_result(
            get_json_resp(sq_m.query, page))

    except JSONDecodeError as err:
        return sq_m

    with models.db.session.no_autoflush:  # pylint: disable=no-member
        for match in matches:
            imgres_url_query = parse_qs(urlparse(match['imgres_url']).query)
            img_url_kwargs = {
                'url': imgres_url_query.get('imgurl', [None])[0],
                'width': imgres_url_query.get('w', [None])[0],
                'height': imgres_url_query.get('h', [None])[0],
            }
            img_url_m, _ = models.get_or_create(
                models.db.session, models.ImageURL, **img_url_kwargs)
            thumb_url_kwargs = {
                'url': match['json_data']['tu'],
                'width': match['json_data']['tw'],
                'height': match['json_data']['th'],
            }
            thumb_url_m, _ = models.get_or_create(
                models.db.session, models.ImageURL, **thumb_url_kwargs)
            match['img_url'] = img_url_m.url
            match['thumb_url'] = thumb_url_m.url
            match_in_sq_m = [
                x for x in sq_m.match_results
                if x.json_data_id == match['json_data_id']]
            if match_in_sq_m:
                if len(match_in_sq_m) > 1:
                    app.logger.debug(
                        'Found %s match result with same json data',
                        len(match_in_sq_m)
                    )
                assert match_in_sq_m[0].json_data == match['json_data']
                match_m = match_in_sq_m[0]
            else:
                match_m, _ = models.get_or_create(
                    models.db.session, models.MatchResult, **match)
            sq_m.match_results.append(match_m)
    models.db.session.add(sq_m)  # pylint: disable=no-member
    models.db.session.commit()  # pylint: disable=no-member
    return sq_m


def get_or_create_search_query(search_query, page, use_cache=True):
    """Get or create search query model."""
    current_datetime = datetime.datetime.now()
    sq_kwargs = {
        'query': search_query, 'page': page,
        'query_url': get_json_resp_query_url(search_query, page)
    }
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
    sq_m = cache_search_query(sq_m)
    return sq_m, sq_created


@app.route('/u/', methods=['GET', 'POST'], defaults={'page': 1})
@app.route('/u/p/<int:page>')
def image_url_view(page=1):
    """View for image url."""
    search_url = request.args.get('u', None)
    return render_template('image_url.html', entries=[search_url], page=page)


@app.route('/', methods=['GET', 'POST'], defaults={'page': 1})
@app.route('/p/<int:page>')
# @vcr.use_cassette(record_mode='new_episodes')
def index(page=1):
    """Get Index page."""
    form = IndexForm()
    entry = None
    search_query = request.args.get('query', None)
    disable_image = request.args.get('disable_image', None)
    limit = request.args.get('limit', None)
    render_template_kwargs = {'form': form, 'entry': entry}
    page_from_query = request.args.get('page', None)
    if page_from_query:
        page = int(page_from_query)

    if search_query:
        pass
    elif form.validate_on_submit():
        search_query = form.query.data
        disable_image = form.disable_image.data
        limit = form.limit.data
    elif form.is_submitted() and not form.validate():
        flash('Form is invalid.', 'danger')
        return render_template('index.html', **render_template_kwargs)
    else:
        return render_template('index.html', **render_template_kwargs)

    sq_m, _ = get_or_create_search_query(search_query, page - 1)
    app.logger.debug(
        '%s match(s) found for [%s]', len(sq_m.match_results), sq_m.query)
    entry = sq_m

    try:
        if limit is not None:
            limit = int(limit)
            if limit > 0:
                pass
            else:
                app.logger.debug('Unexpected limit, so reset the limit')
                flash("Unexpected limit, limit disabled.", 'warning')
                limit = None
    except Exception as err:  # pylint: disable=broad-except
        app.logger.error('Error when parsing limit. err:%s', err)
        flash("Limit Error, limit disabled.", 'warning')
        limit = None

    if entry and entry.match_results and limit:
        if limit > len(entry.match_results):
            limit = len(entry.match_results)
            msg = 'limit is capped at {}'.format(limit)
            app.logger.debug(msg)
            flash(msg, 'warning')

    def return_page_url(page_input):
        """Return page url."""
        url = url_for('index', page=page_input)
        q_dict = {}
        if search_query:
            q_dict['query'] = search_query
        if limit:
            q_dict['limit'] = limit
        if disable_image:
            q_dict['disable_image'] = disable_image
        if q_dict:
            url += '?' + urlencode(q_dict)
        return url

    app.logger.debug('Limit: %s', limit)
    render_template_kwargs.update({
        'form': form, 'entry': entry,
        'pagination': pagination.Pagination(page, return_page_url),
        'disable_image': disable_image, 'limit': limit
    })
    return render_template('index.html', **render_template_kwargs)


def parse_json_resp_for_match_result(response):  # pylint: disable=invalid-name
    """Parse json response for match result."""
    soup = BeautifulSoup(response, 'html.parser')
    for match in soup.select('.rg_bx'):
        imgres_url = match.select_one('a').get('href', None)
        imgref_url = parse_qs(
            urlparse(imgres_url).query).get('imgrefurl', [None])[0]
        json_data = json.loads(match.select_one('.rg_meta').text)
        if json_data['msu'] != json_data['si']:
            app.logger.warning(
                ''.join(ndiff([json_data['msu']], [json_data['si']])))

        match_result = {
            'data_ved': match.get('data-ved', None),
            'imgres_url': imgres_url,
            'imgref_url': imgref_url,
            # json data
            'json_data': json_data,
            'json_data_id': json_data['id'],
            'picture_title': json_data['pt'],
            'site': json_data['isu'],
            'site_title': json_data.get('st', None),
            'img_ext': json_data['ity'],
            'json_search_url': urljoin('https://www.google.com', json_data['msu'])
        }
        yield match_result


def shell_context():
    """Return shell context."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    models.db.init_app(app)
    return {'app': app, 'db': models.db, 'models': models, }


def create_app(script_info=None):  # pylint: disable=unused-argument
    """Create app."""
    app.shell_context_processor(shell_context)
    if not app.debug:
        directory = 'log'
        if not os.path.exists(directory):
            os.makedirs(directory)
        default_log_file = os.path.join(
            directory, 'google_images_download_server.log')
        file_handler = TimedRotatingFileHandler(
            default_log_file, 'midnight')
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(
            logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
        app.logger.addHandler(file_handler)

    app_admin = Admin(app, name='google image download', template_mode='bootstrap3')
    app_admin.add_view(ModelView(models.SearchQuery, models.db.session))
    app_admin.add_view(ModelView(models.MatchResult, models.db.session))
    app_admin.add_view(ModelView(models.ImageURL, models.db.session))
    Bootstrap(app)
    return app


@click.group()
def cli():
    """CLI command."""
    pass


@cli.command()
@click.option("-h", "--host", default="127.0.0.1", type=str)
@click.option("-p", "--port", default=5000, type=int)
@click.option("-d", "--debug", is_flag=True)
@click.option("-r", "--reloader", is_flag=True)
def run(host='127.0.0.1', port=5000, debug=False, reloader=False):
    """Run the application server."""
    if reloader:
        app.jinja_env.auto_reload = True
        app.config["TEMPLATES_AUTO_RELOAD"] = True

    # logging
    directory = 'log'
    if not os.path.exists(directory):
        os.makedirs(directory)
    default_log_file = os.path.join(
        directory, 'google_images_download_server.log')
    file_handler = TimedRotatingFileHandler(
        default_log_file, 'midnight')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(
        logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
    app.logger.addHandler(file_handler)

    api_manager = APIManager(app, flask_sqlalchemy_db=models.db)
    api_manager.create_api(models.SearchQuery, methods=['GET'])
    api_manager.create_api(models.MatchResult, methods=['GET'])
    app_admin = Admin(app, name='google image download', template_mode='bootstrap3')
    app_admin.add_view(admin.SearchQueryView(models.SearchQuery, models.db.session))
    app_admin.add_view(admin.MatchResultView(models.MatchResult, models.db.session))
    app_admin.add_view(ModelView(models.ImageURL, models.db.session))
    app_admin.add_view(ModelView(models.Tag, models.db.session))
    Bootstrap(app)

    if debug:
        app.config.from_object('google_images_download.server_debug_config')
        models.db.init_app(app)
        app.app_context().push()
        models.db.create_all()
        logging.basicConfig(level=logging.DEBUG)

    app.run(
        host=host, port=port,
        debug=debug, use_debugger=debug,
        use_reloader=reloader,
    )


if __name__ == '__main__':
    cli()
