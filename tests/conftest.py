from pathlib import Path

import pytest


SYNTAX_FIXTURES = (Path(__file__).parent / 'syntax').resolve()
SYNTAX_IDL_FIXTURES = SYNTAX_FIXTURES / 'idl'
SYNTAX_EXPECTED_FIXTURES = SYNTAX_FIXTURES / 'baseline'


@pytest.fixture(params=[
    fixture.name
    for fixture in SYNTAX_IDL_FIXTURES.glob('*.webidl')
    if fixture.is_file()
])
def syntax_fixture(request):
    webidl = SYNTAX_IDL_FIXTURES / request.param
    expected = (SYNTAX_EXPECTED_FIXTURES / request.param).with_suffix('.json')

    return webidl, expected
