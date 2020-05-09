from typing import Iterable

import click

from .productions import Parser, Scanner
from .productions.node import Node
from .visitors import Walker


@click.command()
@click.option('--action', '-a',
              default='parse',
              type=click.Choice(('parse', 'validate')))
def cli(action):
    print(action)


def validate(_: str) -> bool:
    pass


def walk(node: Node) -> Iterable[Node]:
    return Walker().visit(node)


def parse(text: str):
    scanner = Scanner(text)
    parser = Parser(scanner.tokens)

    return parser.parse()
