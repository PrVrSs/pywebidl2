import pprint
from pathlib import Path

import attr
import click

from .antlr_visitor import Visitor, parse


def validate(_: str) -> bool:
    pass


def pretty_parse(text: str):
    return [
        attr.asdict(definition)
        for definition in Visitor(parse(text)).run()
    ]


_actions = {
    'parse': pretty_parse,
    'validate': validate,
}


@click.command()
@click.option('--action', '-a',
              default='parse',
              type=click.Choice(_actions.keys()))
@click.option('--file', '-f',
              required=True,
              type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def cli(action, file):
    pprint.pprint(_actions[action](Path(file).read_text()))
