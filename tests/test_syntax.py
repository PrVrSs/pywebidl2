import json

from pywebidl2 import parse_as_dict


def test_syntax(syntax_fixture):
    with syntax_fixture.baseline.open() as expected:
        assert parse_as_dict(syntax_fixture.idl)['definitions'] == json.load(expected)
