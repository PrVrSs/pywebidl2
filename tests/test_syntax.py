from pywebidl2.tokeniser import Scanner
from pywebidl2.parser import Parser
from pywebidl2.ast_printer import JSONPrinter

import json


def test_syntax(syntax_fixture):
    target_file, expected_file = syntax_fixture

    scanner = Scanner(target_file.read_text())
    parser = Parser(scanner.tokens)

    with expected_file.open() as expected:
        assert [
            JSONPrinter().print(defin) for defin in parser.parse()
        ] == json.load(expected)
