import pprint

import click

from .idl import validate, parse_as_dict


_actions = {
    'parse': parse_as_dict,
    'validate': validate,
}


@click.command()
@click.option('--action', '-a',
              default='parse',
              type=click.Choice(tuple(_actions.keys())))
@click.option('--file', '-f',
              required=True,
              type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def cli(action, file):
    pprint.pprint(_actions[action](file))  # pragma: no cover
