import json

from pywebidl2 import JSONPrinter, Parser, Scanner


def test_syntax(syntax_fixture):
    idl, baseline = syntax_fixture

    scanner = Scanner(idl.read_text())
    parser = Parser(scanner.tokens)

    with baseline.open() as expected:
        assert [
            JSONPrinter().print(definition) for definition in parser.parse()
        ] == json.load(expected)
