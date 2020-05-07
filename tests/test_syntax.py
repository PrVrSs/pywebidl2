import json

from pywebidl2 import JSONPrinter, parse


def test_syntax(syntax_fixture):
    idl, baseline = syntax_fixture

    definitions = parse(idl.read_text())

    with baseline.open() as expected:
        assert [
            JSONPrinter().visit(definition) for definition in definitions
        ] == json.load(expected)
