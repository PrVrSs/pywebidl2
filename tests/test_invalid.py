import json

from pywebidl2 import validate


def test_invalid(invalid_fixture):
    with invalid_fixture.baseline.open() as expected:
        assert [
            error._asdict() for error in validate(invalid_fixture.idl.read_text())
        ] == json.load(expected)
