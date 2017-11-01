"""Server module."""
from logging.handlers import TimedRotatingFileHandler
from urllib.parse import urlencode
import logging  # pylint: disable=ungrouped-imports
import os
import shutil
import tempfile

from flask import Flask, render_template, request, url_for, flash, send_from_directory
from flask_restless import APIManager  # pylint: disable=import-error
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
import click

from google_images_download.forms import IndexForm
from google_images_download import models, pagination, admin


app = Flask(__name__)  # pylint: disable=invalid-name

vcr_log = logging.getLogger("vcr")  # pylint: disable=invalid-name
vcr_log.setLevel(logging.INFO)


@app.route('/u/', methods=['GET', 'POST'], defaults={'page': 1})
@app.route('/u/p/<int:page>')
def image_url_view(page=1):
    """View for image url."""
    search_url = request.args.get('u', None)
    entries = [  # pylint: disable=no-member
        models.ImageURL.query.filter_by(url=search_url).one_or_none()]
    return render_template('image_url.html', entries=entries, page=page)


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

    sq_m, created = models.SearchQuery.get_or_create_from_query(search_query, page - 1)
    if created or not sq_m.match_results:
        sq_m.get_match_results()
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


@app.route('/t/<path:filename>')
def thumbnail(filename):
    """Thumbnail url."""
    return send_from_directory(models.THUMB_FOLDER, filename)


@app.route('/f/')
# @vcr.use_cassette(record_mode='new_episodes')
def from_file_search_page():
    """Get search page using google url."""
    file_path = request.args.get('file', None)
    search_type = request.args.get('search_type', 'similar')
    render_template_kwargs = {}
    if not file_path:
        return render_template(
            'google_images_download/from_file_search_page.html',
            entry=None, **render_template_kwargs)

    with tempfile.NamedTemporaryFile() as temp:
        shutil.copyfile(file_path, temp.name)
        entry, _ = models.SearchModel.get_or_create_from_file(temp.name, search_type)
        if not entry.search_file.thumbnail:
            entry.search_file.create_thumbnail(temp.name)
    return render_template(
        'google_images_download/from_file_search_page.html', entry=entry, **render_template_kwargs)


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
