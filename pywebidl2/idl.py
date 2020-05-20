from functools import reduce
from typing import Any, NamedTuple

from antlr4 import CommonTokenStream, FileStream, BailErrorStrategy
from antlr4.error.ErrorListener import ErrorListener

from .generated import WebIDLLexer, WebIDLParser


class SyntaxErrorInfo(NamedTuple):

    line: int
    column: int
    message: str

    def __repr__(self):
        return f'{self.line}:{self.column} {self.message}'


class Idl:

    def __init__(self, file):
        self._parser = Parser(file)

    def parse(self):
        return self._parser.parse()

    def validate(self):
        return self._parser.validate()


class WebIDLErrorListener(ErrorListener):
    def __init__(self):
        self._errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self._errors.append(SyntaxErrorInfo(line, column, msg))

    @property
    def errors(self):
        return self._errors


class Parser:

    def __init__(self, file):

        self._parser = self._build_parser(file)
        self._error_listener = self._setup_listener()

    def _setup_listener(self):
        self._parser.removeErrorListeners()
        self._parser.addErrorListener(error_listener := WebIDLErrorListener())

        return error_listener

    @staticmethod
    def _build_parser(file: str) -> Any:
        functions = (
            FileStream,
            WebIDLLexer,
            CommonTokenStream,
            WebIDLParser,
        )

        return reduce(lambda acc, func: func(acc), functions, file)

    def parse(self):
        self._parser._errHandler = BailErrorStrategy()
        return self._parser.webIDL()

    def validate(self):
        self._parser.webIDL()
        return self._error_listener.errors
