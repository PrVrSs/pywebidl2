import pprint

import click

from .idl import validate, parse


_actions = {
    'parse': parse,
    'validate': validate,
}


@click.command()
@click.option('--action', '-a',
              default='parse',
              type=click.Choice(tuple(_actions.keys())))
@click.argument('file',
                type=click.File(mode='r', encoding='utf-8'))
def cli(action, file):
    pprint.pprint(_actions[action](file.read()))  # pragma: no cover
