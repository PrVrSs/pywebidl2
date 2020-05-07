from .tokeniser import Scanner
from .parser import Parser


def parse(text: str):
    scanner = Scanner(text)
    parser = Parser(scanner.tokens)

    return parser.parse()
