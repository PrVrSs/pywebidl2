from pywebidl2 import validate


def test_syntax(invalid_fixture):
    actual = list(map(str, validate(invalid_fixture.idl)))
    expected = invalid_fixture.baseline.read_text().splitlines()

    assert actual == expected
