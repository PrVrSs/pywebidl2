import json

from pywebidl2 import parse


def test_syntax(syntax_fixture):
    with syntax_fixture.baseline.open() as expected:
        assert parse(syntax_fixture.idl.read_text())['definitions'] == json.load(expected)
