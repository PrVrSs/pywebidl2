import pprint

import attr
import click

from .antlr_visitor import Visitor
from .idl import Idl


def validate(file: str):
    if errors := Idl(file).validate():
        return errors

    return 'Ok'


def pretty_parse(file: str):
    return [
        attr.asdict(definition)
        for definition in Visitor(Idl(file).parse()).run()
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
    pprint.pprint(_actions[action](file))  # pragma: no cover
