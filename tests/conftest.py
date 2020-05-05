from pathlib import Path

import pytest


SYNTAX_FIXTURES = (Path(__file__).parent / 'syntax').resolve()
SYNTAX_IDL_FIXTURES = SYNTAX_FIXTURES / 'idl'
SYNTAX_BASELINE_FIXTURES = SYNTAX_FIXTURES / 'baseline'


@pytest.fixture(params=[
    fixture.name for fixture in SYNTAX_IDL_FIXTURES.glob('*.webidl')
])
def syntax_fixture(request):
    idl = SYNTAX_IDL_FIXTURES / request.param
    baseline = (SYNTAX_BASELINE_FIXTURES / request.param).with_suffix('.json')

    return idl, baseline
