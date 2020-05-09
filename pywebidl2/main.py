import pprint
from pathlib import Path
from typing import Iterable

import click

from .productions import Parser, Scanner
from .productions.node import Node
from .visitors import Walker, JsonView


def validate(_: str) -> bool:
    pass


def walk(node: Node) -> Iterable[Node]:
    return Walker().visit(node)


def parse(text: str):
    return Parser(Scanner(text).tokens).parse()


def pretty_parse(text: str):
    return [JsonView().visit(definition) for definition in parse(text)]


actions = {
    'parse': pretty_parse,
    'validate': validate,
}


@click.command()
@click.option('--action', '-a',
              default='parse',
              type=click.Choice(actions.keys()))
@click.option('--file', '-f',
              required=True,
              type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def cli(action, file):
    pprint.pprint(actions[action](Path(file).read_text()))
