import json

from pywebidl2 import validate


def test_syntax(invalid_fixture):
    with invalid_fixture.baseline.open() as expected:
        assert [
            error._asdict()
            for error in validate(invalid_fixture.idl)
        ] == json.load(expected)
