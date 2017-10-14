"""Admin module."""
from urllib.parse import parse_qs, urlparse

from flask_admin.contrib.sqla import ModelView
from jinja2 import Markup


def url_formatter(_, __, model, name):
    """URL formatter."""
    input_url = getattr(model, name)
    if not input_url:
        formatted_url = ''
    else:
        parsed_url = urlparse(input_url)
        formatted_url = parsed_url.netloc
        formatted_url += parsed_url.path
        formatted_url += '<br/>'
        if parsed_url.query:
            formatted_q = parse_qs(parsed_url.query)
            formatted_url += '?'
            for key, values in formatted_q.items():
                for val in values:
                    if val.startswith(('https://', 'http://')):
                        formatted_url += '{}=<a href="{}">{}</a>'.format(
                            key, val, val)
                    else:
                        formatted_url += '{}={}'.format(key, val)
                    formatted_url += '<br/>'
        if parsed_url.fragment:
            formatted_url += '#'
            formatted_url += parsed_url.fragment
    return Markup(
        "<a href='%s'>[link]</a><br/>%s" % (input_url, formatted_url)
    ) if input_url else ""


def json_formatter(_, __, model, name):
    """URL formatter."""
    json_input = getattr(model, name)
    result = ''
    for key, val in sorted(json_input.items()):
        val_str = str(val)
        if val_str.startswith('/search?'):
            str_templ = '{}: <a href="https://www.google.com{}">{}</a><br/>'
            result += str_templ.format(
                str(key), val_str, val_str)
        elif val_str.startswith(('https://', 'http://')):
            result += '{}: <a href="{}">{}</a><br/>'.format(
                str(key), val_str, val_str)
        else:
            result += '{}: {}<br/>'.format(str(key), val_str)
    return Markup(result)


class SearchQueryView(ModelView):
    """Custom view for SearchQuery model."""
    column_formatters = {
        'query_url': url_formatter
    }


class MatchResultView(ModelView):
    """Custom view for MatchResult model."""
    column_formatters = {
        'imgres_url': url_formatter,
        'json_data': json_formatter,
    }
