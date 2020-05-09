import json

from pywebidl2 import pretty_parse


def test_syntax(syntax_fixture):
    idl, baseline = syntax_fixture

    with baseline.open() as expected:
        assert pretty_parse(idl.read_text()) == json.load(expected)
