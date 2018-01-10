"""Server module."""
from logging.handlers import TimedRotatingFileHandler
from urllib.parse import urlencode, parse_qs, urlparse
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

from google_images_download.forms import IndexForm, FileForm
from google_images_download import models, pagination, admin


app = Flask(__name__)  # pylint: disable=invalid-name


@app.route('/u/', methods=['GET', 'POST'], defaults={'page': 1})
@app.route('/u/p/<int:page>')
def image_url_view(page=1):
    """View for image url."""
    search_url = request.args.get('u', None)
    entries = [  # pylint: disable=no-member
        models.ImageURL.query.filter_by(url=search_url).one_or_none()]
    return render_template(
        'google_images_download/image_url.html', entries=entries, page=page, search_url=search_url)


@app.route('/')
def index():
    """Get Index page."""
    form = IndexForm(request.args)
    search_query = form.query.data
    limit = form.limit.data
    entry = None
    render_template_kwargs = {'form': form, 'entry': entry}
    page = form.page.data if form.page.data else 1
    if not search_query:
        return render_template('index.html', **render_template_kwargs)

    sq_m, _ = models.SearchQuery.get_or_create_from_query(search_query, page - 1)
    if not sq_m.match_results:
        sq_m.get_match_results()
    app.logger.debug(
        '%s match(s) found for [%s] page:%s', len(sq_m.match_results), sq_m.query, page)
    entry = sq_m

    entry_match_results = entry.match_results
    if limit and limit < len(entry.match_results):
        entry_match_results = entry.match_results[:limit]
    render_template_kwargs['entry_match_results'] = entry_match_results

    def return_page_url(page_input):
        """Return page url."""
        url_query = parse_qs(urlparse(request.url).query)
        url_query['page'] = [page_input]
        new_query = urlencode(url_query, True)
        parsed_url = urlparse(url_for('index'))
        parsed_url = parsed_url._replace(query=new_query)
        return parsed_url.geturl()

    app.logger.debug('Limit: %s', limit)
    render_template_kwargs.update({
        'form': form, 'entry': entry,
        'pagination': pagination.Pagination(page, return_page_url),
        'limit': limit
    })
    return render_template('index.html', **render_template_kwargs)


@app.route('/t/<path:filename>')
def thumbnail(filename):
    """Thumbnail url."""
    return send_from_directory(models.THUMB_FOLDER, filename)


@app.route('/f/')
def from_file_search_page():
    """Get search page using google url."""
    form = FileForm(request.args)
    file_path = form.file_path.data
    search_type = form.search_type.data
    disable_cache = form.disable_cache.data
    render_template_kwargs = {'entry': None, 'form': form}
    file_exist = os.path.isfile(file_path) if file_path is not None else False
    empty_response = render_template(
        'google_images_download/from_file_search_page.html', **render_template_kwargs)

    if not file_path or not file_exist:
        if not file_exist:
            app.logger.debug('File not exist:%s', file_path)
        return empty_response
    with tempfile.NamedTemporaryFile() as temp:
        shutil.copyfile(file_path, temp.name)
        try:
            entry, _ = models.SearchModel.get_or_create_from_file(
                temp.name, search_type, use_cache=not disable_cache)
            if not entry.search_file.thumbnail:
                entry.search_file.create_thumbnail(temp.name)
        except Exception as err:  # pylint: disable=broad-except
            flash('{} raised:{}'.format(type(err), err), 'danger')
            return empty_response
    app.logger.debug('[%s],[%s],file:%s', search_type, len(entry.match_results), file_path)
    app.logger.debug('URL:%s', request.url)
    render_template_kwargs['entry'] = entry
    return render_template(
        'google_images_download/from_file_search_page.html', **render_template_kwargs)


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
@click.option("-t", "--threaded", is_flag=True)
def run(host='127.0.0.1', port=5000, debug=False, reloader=False, threaded=False):
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
    app_admin.add_view(admin.ImageURLView(models.ImageURL, models.db.session))
    # app_admin.add_view(ModelView(models.Tag, models.db.session))  # not used yet
    app_admin.add_view(admin.ImageFileView(models.ImageFile, models.db.session))
    app_admin.add_view(admin.SearchFileView(models.SearchFile, models.db.session))
    app_admin.add_view(admin.SearchModelView(models.SearchModel, models.db.session))
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
        threaded=threaded
    )


if __name__ == '__main__':
    cli()
