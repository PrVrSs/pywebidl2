from more_itertools.more import peekable
from more_itertools.recipes import first_true

from .errors import WebIDLParseError
from .expressions import Identifier, IdentifierList
from .statement import ExtendedAttribute, Interface
from .token_type import TokenType


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

        return definitions

    def definition(self):
        extended_attrs = list(self.extended_attributes())

        return Interface(
            name='',
            inheritance='',
            ext_attrs=extended_attrs,
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


# [Global=(Worker,ServiceWorker), Exposed=ServiceWorker]

# [IntAttr=0, FloatAttr=3.14, StringAttr="abc", IdentifierAttr=_null, IdentifiersAttr=(_null, _const), FloatList=(3.14)]
# [
#     Constructor,
#     Constructor(double radius)
# ]

# [Exposed=Window]