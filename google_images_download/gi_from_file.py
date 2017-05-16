#!/usr/bin/env python3
"""google image related function.

modified version from
http://stackoverflow.com/a/28792943
"""
import webbrowser

import requests
import click


@click.command()
@click.argument('file_path', click.Path(exists=True))
def search(file_path):
    """Simple program that search image."""
    search_url = 'http://www.google.hr/searchbyimage/upload'
    multipart = {'encoded_image': (file_path, open(file_path, 'rb')), 'image_content': ''}
    response = requests.post(search_url, files=multipart, allow_redirects=False)
    fetch_url = response.headers['Location']
    webbrowser.open(fetch_url)


if __name__ == '__main__':
    search()
