import pprint

import attr
import click

from .antlr_visitor import Visitor
from .idl import Idl


def validate(file: str):
    return Idl(file).validate()


def pretty_parse(file: str):
    ast = Visitor(Idl(file).parse()).run()

    return [
        attr.asdict(definition)
        for definition in ast.definitions
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
