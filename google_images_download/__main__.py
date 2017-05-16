#!/usr/bin/env python3
import click


@click.group()
def cli():
    pass


@click.command()
def download(keywords):
    click.echo('dowload')

def search(filepath):
    click.echo('search')
