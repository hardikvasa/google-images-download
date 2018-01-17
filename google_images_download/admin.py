"""Admin module."""
from urllib.parse import parse_qs, urlparse
import textwrap

from flask import request, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_paginate import get_page_parameter, Pagination
from jinja2 import Markup
import humanize
import structlog

from google_images_download import forms, models, api


log = structlog.getLogger(__name__)


def url_formatter(_, __, model, name):
    """URL formatter."""
    input_url = getattr(model, name)
    if not input_url:
        formatted_url = ''
    else:
        parsed_url = urlparse(input_url)
        formatted_url = '<tr><th>Netloc</th><td>{}</td></tr>'.format(parsed_url.netloc)
        formatted_url += '<tr><th>Path</th><td>{}</td></tr>'.format(parsed_url.path)
        if parsed_url.fragment:
            formatted_url += '<tr><th>fragment</th><td>{}</td></tr>'.format(parsed_url.fragment)
        if parsed_url.query:
            formatted_url += '<tr><th colspan="2">Query</th></tr>'
            formatted_q = parse_qs(parsed_url.query)
            for key, values in formatted_q.items():
                for val in values:
                    if val.startswith(('https://', 'http://')):
                        template = '<tr><th>{0}</th><td><a href="{1}">{1}</a></td></tr>'
                        formatted_url += template.format(key, val)
                    else:
                        formatted_url += '<tr><th>{}</th><td>{}</td></tr>'.format(key, val)
        template = '<table class="table table-bordered table-condensed">{}</table>'
        formatted_url = template.format(formatted_url)
    return Markup(
        "<a href='{}'>[link]</a><br/>{}".format(input_url, formatted_url)
    ) if input_url and input_url != '#' else Markup("")


def json_formatter(_, __, model, name):
    """URL formatter."""
    json_input = getattr(model, name)
    result = ''
    for key, val in sorted(json_input.items()):
        val_str = str(val)
        if val_str.startswith('/search?'):
            str_templ = '<tr><th>{}</th><td><a href="https://www.google.com{}">{}</a></td></tr>'
            result += str_templ.format(
                str(key), val_str, val_str)
        elif val_str.startswith(('https://', 'http://')):
            result += '<tr><th>{}</th><td><a href="{}">{}</a></td></tr>'.format(
                str(key), val_str, val_str)
        else:
            result += '<tr><th>{}</th><td>{}</td></tr>'.format(str(key), val_str)
    result = '<table class="table table-bordered table-condensed">{}</table>'.format(result)
    return Markup(result)


def date_formatter(_, __, model, name):
    date_data = getattr(model, name)
    humanized_date_data = humanize.naturaltime(date_data)
    return Markup(
        '<span data-toogle="tooltip" title="{}">{}</span>'.format(
            date_data, humanized_date_data
        )
    )


def filesize_formatter(_, __, model, name):
    data = getattr(model, name)
    if data:
        return Markup(humanize.naturalsize(data))
    return Markup('')


class HomeView(AdminIndexView):
    @expose('/')
    def index(self):
        form = forms.IndexForm(request.args)
        page = request.args.get(get_page_parameter(), type=int, default=1)
        query = form.query.data
        disable_cache = form.disable_cache.data
        template_kwargs = {'entry': None, 'query': query, 'form': form, }
        pagination_kwargs = {'page': page, 'show_single_page': False, 'bs_version': 3, }
        if query:
            pagination_kwargs['per_page'] = 1
            model, created = api.get_or_create_search_query(
                query, page, disable_cache=disable_cache)
            if created or disable_cache:
                models.db.session.add(model)
                models.db.session.commit()
            pagination_kwargs['total'] = \
                models.SearchQuery.query.filter(models.SearchQuery.search_query == query).count()
            template_kwargs['entry'] = model
        template_kwargs['pagination'] = Pagination(**pagination_kwargs)
        return self.render('google_images_download/index.html', **template_kwargs)


class SearchQueryView(ModelView):
    """Custom view for SearchQuery model."""
    can_view_details = True
    column_formatters = {'created_at': date_formatter, }
    column_searchable_list = ('page', 'search_query')
    column_filters = ('page', 'search_query')


class MatchResultView(ModelView):
    """Custom view for MatchResult model."""

    def _image_formatter(view, context, model, name):
        desc_table = '<tr><th>Title</th><td>{}</td></tr>'.format(model.picture_title)
        if model.picture_subtitle:
            desc_table += '<tr><th>Subtitle</th><td>{}</td></tr>'.format(model.picture_subtitle)
        desc_table += '<tr><th>Site</th><td><a href="https://{0}">{0}</a></td></tr>'.format(
            model.site)
        desc_table += '<tr><th>Site title</th><td>{}</td></tr>'.format(model.site_title)
        desc_table = '<table class="table table-condensed table-bordered">{}</table>'.format(
            desc_table)
        template = '<a href="{1}"><img class="img-responsive center-block" src="{0}"></a><br>{2}'
        return Markup(template.format(model.thumb_url, model.img_url, desc_table))

    def _thumbnail_formatter(view, context, model, name):
        templ = '<a href="{1}"><img src="{0}"></a>'
        if model.img_url:
            return Markup(templ.format(model.thumbnail_url.url, model.img_url.url))
        return Markup(templ.format(model.thumbnail_url.url, model.thumbnail_url.url))

    column_formatters = {'created_at': date_formatter, 'thumbnail_url': _thumbnail_formatter, }
    column_exclude_list = ('imgres_url', 'img_url',)
    can_view_details = True
    page_size = 100


class JSONDataView(ModelView):
    """Custom view for json data model"""
    def _value_formatter(view, context, model, name):
        res = ''
        for key, value in model.value.items():
            res += '<tr><th>{0}</th><td>{1}</td></tr>'.format(key, value)
        res = '<table class="table table-bordered table-condensed">{}</table>'.format(res)
        return Markup(res)
    can_view_details = True
    column_formatters = {'created_at': date_formatter, 'value': _value_formatter, }


class ImageURLView(ModelView):
    """Custom view for ImageURL model."""

    def _url_formatter(view, context, model, name):
        match_results = model.match_results
        templ = """
        <figure>
        <a href="{3}"><img src="{1}"></a>
        <figcaption><a href="{0}">{2}</figcaption>
        <figure>"""
        img_view_url = url_for('u.index', u=model.url)
        if match_results:
            first_match_result = next(iter(match_results or []), None)
            shorted_url = '<br>'.join(textwrap.wrap(model.url))
            return Markup(
                templ.format(
                    model.url,
                    first_match_result.thumbnail_url.url,
                    shorted_url,
                    img_view_url
                )
            )
        shorted_url = '<br>'.join(textwrap.wrap(model.url))
        return Markup(templ.format(model.url, model.url, shorted_url, img_view_url))

    can_view_details = True
    column_searchable_list = ('url', 'width', 'height')
    column_filters = ('width', 'height')
    column_formatters = {'created_at': date_formatter, 'url': _url_formatter, }
    page_size = 100
    column_default_sort = ('created_at', True)


class TagView(ModelView):
    """Custom view for Tag model."""

    column_searchable_list = ('namespace', 'name')
    column_filters = ('namespace', 'name')
    column_formatters = {'created_at': date_formatter, }
    column_default_sort = ('created_at', True)
    page_size = 100


class ImageFileView(ModelView):
    """Custom view for ImageFile model."""

    def _thumbnail_formatter(view, context, model, name):
        if not model.thumbnail:
            return
        return Markup('<img src="{}">'.format(url_for(
            'thumbnail', filename=model.thumbnail.checksum + '.jpg')))

    column_formatters = {
        'created_at': date_formatter,
        'size': filesize_formatter,
        'thumbnail': _thumbnail_formatter,
    }
    can_view_details = True
    page_size = 100


class SearchImageView(ModelView):
    """Custom view for SearchImage model."""

    def _result_formatter(view, context, model, name):
        res = '<a href="{}">main</a>'.format(model.search_url)
        if model.size_search_url:
            res += ', <a href="{}">size</a>'.format(model.size_search_url)
        if model.similar_search_url:
            res += ', <a href="{}">similar</a>'.format(model.similar_search_url)
        return Markup(res)

    @staticmethod
    def _format_searched_img_url(url):
        url_text = url
        if not url:
            return
        if url.startswith('https://'):
            url_text = url.replace('https://', '', 1)
        elif url.startswith('http://'):
            url_text = url.replace('http://', '', 1)
        return '<a href="{}">{}</a>'.format(url, url_text)

    def _input_search_formatter(view, context, model, name):
        res = ''
        if model.img_file:
            res += '<p>Image File</p>'
            if model.img_file.thumbnail:
                res += '<figure><img src="{}"><figcaption>{}</figcaption><figure>'.format(
                    url_for('thumbnail', filename=model.img_file.thumbnail.checksum + '.jpg'),
                    Markup.escape(model.img_file)
                )
            else:
                res += '<p>{}</p>'.format(model.img_file)
        if model.searched_img_url:
            res += '<p>Searched Url</p>'
            res += SearchImageView._format_searched_img_url(model.searched_img_url)
        return Markup(res)

    column_formatters = {
        'created_at': date_formatter,
        'Result': _result_formatter,
        'Input': _input_search_formatter,
        'searched_img_url': lambda v, c, m, p: Markup(
            SearchImageView._format_searched_img_url(m.searched_img_url)
            if m.searched_img_url else ''
        ),
    }
    column_exclude_list = (
        'search_url', 'similar_search_url', 'size_search_url', 'searched_img_url', 'img_file', )
    can_view_details = True
    column_searchable_list = ('searched_img_url', )
    column_list = ('img_file', 'created_at', 'searched_img_url', 'img_guess', 'Result', 'Input')


class SearchImagePageView(ModelView):
    """Custom view for SearchImagePage model."""

    column_formatters = dict(
        created_at=date_formatter,
        search_type=lambda v, c, m, p: m.search_type.value
    )
    column_exclude_list = ('search_url', 'similar_search_url', 'size_search_url', )
    can_view_details = True


class TextMatchView(ModelView):
    """Custom view for TextMatch model."""

    can_view_details = True
    column_formatters = {
        'created_at': date_formatter,
        'content': lambda v, c, m, p: Markup(
            '<h4>{0}</h4><p>{1}</p><a href="{2}">{4}</a><p>{3}</p>'.format(
                m.title,
                '<br>'.join(textwrap.wrap(m.text)),
                m.url,
                m.url_text,
                '<br>'.join(textwrap.wrap(m.url)),
            )
        ),
    }
    column_searchable_list = ('url', 'url_text', 'text', 'title')
    column_filters = ('url_text', 'text', 'title')
    column_exclude_list = ('imgres_url', 'imgref_url', )
    column_list = (
        'search_image_model',
        'img_url',
        'thumbnail_url',
        'created_at',
        'content',
    )
    page_size = 50
    column_default_sort = ('created_at', True)


class MainSimilarResultView(ModelView):
    """Custom view for SearchImagePage model."""

    column_formatters = dict(
        created_at=date_formatter,
        img_title=lambda v, c, m, p: Markup('<a href="{0}">{0}</a>'.format(m.img_title))
    )
    column_exclude_list = ('search_url', 'img_src', )
    can_view_details = True
    column_searchable_list = ('img_title', 'img_width', 'img_height')
    column_filters = ('img_title', 'img_width', 'img_height')
