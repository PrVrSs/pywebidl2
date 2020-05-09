from more_itertools.more import peekable
from more_itertools.recipes import first_true

from .node import (
    Argument,
    Attribute,
    ExtendedAttribute,
    Identifier,
    IdentifierList,
    IDLType,
    Interface,
    Iterable_,
    Operation,
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


class Parser(BaseParser):

    def parse(self):
        return list(self.definitions())

    def definitions(self):
        while not self._is_at_end():
            yield self.definition()
            self._consume(TokenType.SEMICOLON, 'Expected ";" after definition')

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
        async_ = self._match(TokenType.ASYNC)

        if self._match(TokenType.ATTRIBUTE):
            return self.attribute()
        elif self._match(TokenType.ITERABLE):
            return self.iterable(async_)

        return Operation(
            idl_type=self.idl_type('return-type'),
            name=self._consume(TokenType.IDENTIFIER, 'Expected variable name'),
            arguments=list(self.argument()),
            ext_attrs=[],
        )

    def attribute(self):
        return Attribute(
            idl_type=self.idl_type(type_='attribute-type'),
            name=self._advance(),  # self._consume(
            # TokenType.IDENTIFIER, 'Expected argument name')
            ext_attrs=[],
        )

    def iterable(self, async_):
        self._consume(TokenType.LEFT_ANGLE, 'Expected "<"')

        idl_type = []
        while not self._match(TokenType.RIGHT_ANGLE):
            idl_type.append(self.idl_type())
            self._match(TokenType.COMMA)

        arguments = list(self.argument())

        return Iterable_(
            async_=async_,
            idl_type=idl_type,
            arguments=arguments,
            ext_attrs=[]
        )

    def argument(self):
        if not self._match(TokenType.LEFT_PAREN):
            return []

        while not self._match(TokenType.RIGHT_PAREN):
            yield Argument(
                ext_attrs=list(self.extended_attributes()),
                optional=self._match(TokenType.OPTIONAL),
                idl_type=self.idl_type(type_='argument-type'),
                name=self._advance(),  # self._consume(
                # TokenType.IDENTIFIER, 'Expected argument name')
            )

            self._match(TokenType.COMMA)

    def idl_type(self, type_=None):
        return IDLType(
            type=type_,
            ext_attrs=list(self.extended_attributes()),
            idl_type=self._consume(TokenType.IDENTIFIER, 'Expected idl type'),

        )

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
            arguments=[],
        )

    def rhs(self):
        if not self._match(TokenType.EQUAL):
            return

        if self._match(TokenType.LEFT_PAREN):
            return self.identifier_list()

        return self.identifier()

    def identifier(self):
        return Identifier(
            value=self._consume(TokenType.IDENTIFIER, 'Expected variable name'))

    def identifier_list(self):
        values = []

        while not self._match(TokenType.RIGHT_PAREN):
            if self._match(TokenType.COMMA):
                continue

            values.append(
                self._consume(TokenType.IDENTIFIER, 'Expected variable name'))

        return IdentifierList(value=values)
