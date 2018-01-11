"""Admin module."""
from urllib.parse import parse_qs, urlparse

from flask_admin.contrib.sqla import ModelView
from jinja2 import Markup
import humanize
import structlog
from flask import url_for


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


class SearchQueryView(ModelView):
    """Custom view for SearchQuery model."""

    can_view_details = True
    column_display_pk = True
    column_formatters = {
        'query_url': url_formatter,
        'created_at': date_formatter,
        'updated_at': date_formatter,
    }
    column_exclude_list = ('query_data', 'updated_at', 'query_url')
    column_searchable_list = ('page', 'query')


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
        return Markup('<a href="{1}"><img src="{0}"></a>'.format(model.thumb_url, model.img_url))

    column_formatters = {
        'created_at': date_formatter,
        'image': _image_formatter,
        'imgres_url': url_formatter,
        'json_data': json_formatter,
        'thumbnail': _thumbnail_formatter,
        'updated_at': date_formatter,
    }
    column_exclude_list = (
        'image_page_url',
        'imgref_url',
        'imgres_url',
        'json_data',
        'json_data_id',
        'json_search_url',
        'picture_subtitle',
        'thumbnail',
        'updated_at',
        'site_title',
        'picture_title',
        'site',
    )
    can_view_details = True
    column_searchable_list = ('picture_subtitle', 'picture_title', 'site_title', 'site')


class ImageURLView(ModelView):
    """Custom view for ImageURL model."""

    def _img_url_formatter(view, context, model, name):
        first_match_result = next(iter(model.match_results or []), None)

        def formatted_caption_url(input_url):
            """format url caption.

            split the urls into 3 parts:

            - domain
            - path
            - others

            path should be rebuild so the longest part of the path should be on on its own line.
            """
            parsed_url = urlparse(input_url)
            domain = '{}://{}'.format(parsed_url[0], parsed_url[1])
            path_parts = parsed_url.path.split('/')
            path_max = max([len(x) for x in path_parts]) + 1  # include slash character
            if len(domain) > path_max:
                path_max = len(domain)
            formatted_path = ''
            temp_path = ''
            last_temp_path = ''
            for item in path_parts[1:]:
                temp_path += '/{}'.format(item)
                if len(temp_path) > path_max:
                    formatted_path += last_temp_path + '<br>'
                    temp_path = '/{}'.format(item)
                last_temp_path = temp_path
            if temp_path:
                formatted_path += temp_path
            domain_and_path_part = '{}://{}{}'.format(
                parsed_url.scheme, parsed_url.netloc, parsed_url.path)
            non_domain_and_path_part = input_url.split(domain_and_path_part, 1)[1]
            return "{}<br>{}<br>{}".format(
                domain, formatted_path, non_domain_and_path_part)

        template = """
        <figure style="display: table;">
          <a href="{1}"><img src="{0}"></a>
          <figcaption style="display: table-caption; caption-side:bottom;">
            <a style="overflow-wrap: break-word; word-wrap: break-word;" href="{2}">{1}</a>
          </figcaption>
        </figure>"""
        if first_match_result:
            return Markup(template.format(
                first_match_result.thumb_url, formatted_caption_url(model.url), model.url))
        return Markup(template.format(
            model.url, formatted_caption_url(model.url), model.url))

    column_exclude_list = ('updated_at',)
    column_display_pk = True
    column_formatters = {
        'url': _img_url_formatter,
        'created_at': date_formatter,
        'updated_at': date_formatter,
    }
    column_searchable_list = ('url', 'width', 'height')
    can_view_details = True


class ImageFileView(ModelView):
    """Custom view for ImageFile model."""

    def _checksum_formatter(view, context, model, name):
        data = getattr(model, name)
        shorten_data = (data[:7] + '...') if len(data) > 7 else data
        first_thumb_search_files = next(iter(model.thumb_search_files or []), None)
        if first_thumb_search_files:
            img_src = url_for('thumbnail', filename=model.checksum + '.jpg')
            return Markup(
                """<figure>
                <img src="{0}">
                <figcaption><span data-toogle="tooltip" title="{2}">{1}</span></figcaption>
                </figure>""".format(img_src, shorten_data, data))
        return Markup(
            '<span data-toogle="tooltip" title="{0}">{1}</span>'.format(data, shorten_data))

    column_display_pk = True
    column_formatters = {
        'created_at': date_formatter,
        'updated_at': date_formatter,
        'size': filesize_formatter,
        'checksum': _checksum_formatter,
    }
    column_exclude_list = ('updated_at',)
    can_view_details = True


class SearchFileView(ModelView):
    """Custom view for SearchFile model."""

    def _thumbnail_formatter(view, context, model, name):
        if hasattr(model, 'thumbnail_basename') and model.thumbnail_basename:
            img_src = url_for('thumbnail', filename=model.thumbnail_basename)
            return Markup('<img src="{}">'.format(img_src))
        if not model.thumb_search_files:
            return Markup('')
        img_src = url_for('thumbnail', filename=model.thumb_search_files[0].thumbnail_basename)
        return Markup('<img src="{}">'.format(img_src))

    def _checksum_formatter(view, context, model, name):
        data = getattr(model, name)
        shorten_data = (data[:7] + '...') if len(data) > 7 else data
        return Markup(
            '<span data-toogle="tooltip" title="{0}">{1}</span>'.format(data, shorten_data))

    column_display_pk = True
    can_view_details = True
    column_exclude_list = ('updated_at', 'search_url', 'similar_search_url', 'size_search_url',)
    column_formatters = {
        'created_at': date_formatter,
        'updated_at': date_formatter,
        'size': filesize_formatter,
        'checksum': _checksum_formatter,
        'thumbnail': _thumbnail_formatter,
    }


class SearchModelView(ModelView):
    """Custom view for SearchModel model."""

    def _search_file_formatter(view, context, model, name):
        data = getattr(model, name)
        shorten_checksum = (data.checksum[:7] + '...') if len(data.checksum) > 7 else data.checksum
        img_src = url_for('thumbnail', filename=data.thumbnail_basename)
        return Markup(
            """<figure>
            <img src="{2}" class="img-responsive center-block">
            <figcaption><span data-toogle="tooltip" title="{0}">{1}</span></figcaption>
            </figure>""".format(data.checksum, shorten_checksum, img_src)
        )

    def _search_type_formatter(view, context, model, name):
        return Markup(getattr(model, name).value)

    can_view_details = True
    column_formatters = {
        'created_at': date_formatter,
        'updated_at': date_formatter,
        'search_type': _search_type_formatter,
        'search_file': _search_file_formatter,
    }
    column_exclude_list = ('query_url', 'page', 'updated_at')
