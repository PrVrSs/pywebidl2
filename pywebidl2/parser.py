from .errors import WebIDLParseError
from .expressions import Identifier
from .statement import ExtendedAttribute
from .token_type import TokenType


class BaseParser:
    def __init__(self, token_list):
        self._current = 0
        self._token_list = token_list

    def _consume(self, token_type, message: str = ''):
        if not self._check(token_type):
            raise WebIDLParseError(message)

        return self._advance()

    def _match(self, *token_types):
        for token in token_types:
            if self._check(token):
                self._advance()

                return True

        return False

    def _check(self, token_type):
        if self._is_at_end():
            return False

        return self._peek().token_type == token_type

    def _advance(self):
        if not self._is_at_end():
            self._current += 1

        return self._previous()

    def _is_at_end(self):
        return self._peek().token_type == TokenType.EOF

    def _is_at_right_paren(self):
        return self._peek().token_type == TokenType.RIGHT_PAREN

    def _is_at_right_square(self):
        return self._peek().token_type == TokenType.RIGHT_SQUARE

    def _is_at_left_square(self):
        return self._peek().token_type == TokenType.LEFT_SQUARE

    def _is_at_right_slash(self):
        return self._peek().token_type == TokenType.SLASH

    def _peek(self):
        return self._token_list[self._current]

    def _previous(self):
        return self._token_list[self._current - 1]


class Parser(BaseParser):

    def parse(self):
        return list(self.definitions())

    def definitions(self):
        while not self._is_at_end():
            yield self.definition()

    def definition(self):
        extended_attrs = list(self.extended_attributes())
        return extended_attrs

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
        if self._match(TokenType.EQUAL):
            return Identifier(
                self._consume(TokenType.IDENTIFIER, 'Expected variable name'))


# [Global=(Worker,ServiceWorker), Exposed=ServiceWorker]

# [IntAttr=0, FloatAttr=3.14, StringAttr="abc", IdentifierAttr=_null, IdentifiersAttr=(_null, _const), FloatList=(3.14)]
# [
#     Constructor,
#     Constructor(double radius)
# ]

# [Exposed=Window]