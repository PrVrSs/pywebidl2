from more_itertools.more import peekable
from more_itertools.recipes import first_true

from .node import (
    ExtendedAttribute,
    Identifier,
    IdentifierList,
    Interface,
    Operation,
    ReturnType,
    Argument,
    ArgumentType,
)
from .token_type import TokenType
from ..errors import WebIDLParseError


class BaseParser:
    def __init__(self, token_list):
        self.tokens = peekable(token_list)

    def _consume(self, token_type, message: str = ''):
        if not self._check(token_type):
            raise WebIDLParseError(message)

        return self._advance()

    def _match(self, *token_types):
        if _ := first_true(token_types, pred=self._check):
            self._advance()

        return _ is not None

    def _check(self, token_type):
        if self._is_at_end():
            return False

        return self.tokens.peek().token_type == token_type

    def _advance(self):
        return next(self.tokens)

    def _is_at_end(self):
        return self.tokens.peek().token_type == TokenType.EOF

    def _is_at_right_paren(self):
        return self.tokens.peek().token_type == TokenType.RIGHT_PAREN

    def _is_at_right_square(self):
        return self.tokens.peek().token_type == TokenType.RIGHT_SQUARE

    def _is_at_left_square(self):
        return self.tokens.peek().token_type == TokenType.LEFT_SQUARE

    def _is_at_right_slash(self):
        return self.tokens.peek().token_type == TokenType.SLASH


class Parser(BaseParser):

    def parse(self):
        return self.definitions()

    def definitions(self):
        definitions = []

        while not self._is_at_end():
            definitions.append(self.definition())
            self._consume(TokenType.SEMICOLON, 'Expected ";"')

        return definitions

    def definition(self):
        extended_attrs = list(self.extended_attributes())

        if self._match(TokenType.INTERFACE):
            return self.interface(extended_attrs)

    def interface(self, extended_attrs):
        name = self._consume(TokenType.IDENTIFIER, 'Expected interface name')
        members = []

        self._consume(TokenType.LEFT_BRACE, 'Expected left brace')

        while not self._match(TokenType.RIGHT_BRACE):
            members.append(self.member())
            self._consume(TokenType.SEMICOLON, 'Expected ";"')

        return Interface(
            name=name,
            ext_attrs=extended_attrs,
            members=members,
        )

    def member(self):
        idl_type = self.return_type()
        name = self._consume(TokenType.IDENTIFIER, 'Expected variable name')

        self._consume(TokenType.LEFT_PAREN, 'Expected "("')

        arguments = []
        while not self._match(TokenType.RIGHT_PAREN):
            arguments.append(self.argument())

        return Operation(name=name, idl_type=idl_type, arguments=arguments)

    def argument(self):
        ext_attrs = list(self.extended_attributes())
        optional = self._match(TokenType.OPTIONAL)
        idl_type = self.argument_type()
        name = self._consume(TokenType.IDENTIFIER, 'Expected argument name')

        return Argument(
            name=name,
            idl_type=idl_type,
            ext_attrs=ext_attrs,
            optional=optional,
        )

    def argument_type(self):
        ext_attrs = list(self.extended_attributes())
        idl_type = self._consume(TokenType.IDENTIFIER, 'Expected variable name')

        return ArgumentType(idl_type=idl_type, ext_attrs=ext_attrs)

    def return_type(self):
        idl_type = self._consume(TokenType.IDENTIFIER, 'Expected variable name')
        return ReturnType(idl_type=idl_type)

    def extended_attributes(self):
        if not self._match(TokenType.LEFT_SQUARE):
            return

        while not self._match(TokenType.RIGHT_SQUARE):
            if self._match(TokenType.COMMA):
                continue

            yield self.extended_attribute()

    def extended_attribute(self):
        return ExtendedAttribute(
            name=self._consume(TokenType.IDENTIFIER, 'Expected variable name'),
            rhs=self.rhs(),
            arguments=None
        )

    def rhs(self):
        if not self._match(TokenType.EQUAL):
            return

        if self._match(TokenType.LEFT_PAREN):
            return self.identifier_list()

        return self.identifier()

    def identifier(self):
        return Identifier(
            self._consume(TokenType.IDENTIFIER, 'Expected variable name'))

    def identifier_list(self):
        values = []

        while not self._match(TokenType.RIGHT_PAREN):
            if self._match(TokenType.COMMA):
                continue

            values.append(
                self._consume(TokenType.IDENTIFIER, 'Expected variable name'))

        return IdentifierList(values)
