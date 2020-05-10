import string
from typing import NamedTuple, List

from .token_type import TokenType


class TokenInfo(NamedTuple):
    type: str
    string: str
    start: int
    end: int
    line: int


class Token:
    def __init__(self, token_type, lexeme: str, literal):
        self.token_type = token_type
        self.lexeme: str = lexeme
        self.literal = literal

    def __repr__(self):
        return f'{self.token_type} {self.lexeme} {self.literal}'


class Scanner:

    _identifier_head = string.ascii_letters + '_-'
    _identifier_body = _identifier_head + string.digits
    _keywords = {
        'interface': TokenType.INTERFACE,
        'optional': TokenType.OPTIONAL,
        'async': TokenType.ASYNC,
        'iterable': TokenType.ITERABLE,
        'attribute': TokenType.ATTRIBUTE,
        'unsigned': TokenType.UNSIGNED,
        'callback': TokenType.CALLBACK,
        'const': TokenType.CONST,
        'Infinity': TokenType.INFINITY,
        'unrestricted': TokenType.UNRESTRICTED,
        'false': TokenType.FALSE,
        'true': TokenType.TRUE,
        'NaN': TokenType.NAN,
    }

    def __init__(self, source: str = ''):
        self.source: str = source
        self.tokens: List[Token] = []
        self._start: int = 0
        self._current: int = 0

        self.scan_tokens()

    def scan_tokens(self):
        while not self._is_at_end():
            self._start = self._current
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, '', None,))

    def _scan_token(self) -> None:
        # pylint: disable=too-many-branches
        char: str = self._advance()

        if char in string.whitespace:
            pass
        elif char == '(':
            self._add_token(TokenType.LEFT_PAREN)
        elif char == ')':
            self._add_token(TokenType.RIGHT_PAREN)
        elif char == '{':
            self._add_token(TokenType.LEFT_BRACE)
        elif char == '}':
            self._add_token(TokenType.RIGHT_BRACE)
        elif char == '[':
            self._add_token(TokenType.LEFT_SQUARE)
        elif char == ']':
            self._add_token(TokenType.RIGHT_SQUARE)
        elif char == '<':
            self._add_token(TokenType.LEFT_ANGLE)
        elif char == '>':
            self._add_token(TokenType.RIGHT_ANGLE)
        elif char == ',':
            self._add_token(TokenType.COMMA)
        elif char == '=':
            self._add_token(TokenType.EQUAL)
        elif char == '-':
            self._add_token(TokenType.MINUS)
        elif char == '+':
            self._add_token(TokenType.PLUS)
        elif char == ';':
            self._add_token(TokenType.SEMICOLON)
        elif char == '"':
            self._constant()
        elif self._is_identifier(char):
            self._identifier()
        elif char.isdigit():
            self._number()
        elif char == '/':
            if self._match('/'):
                self._comment()

    def _comment(self):
        while self._peek() != '\n' and not self._is_at_end():
            self._advance()

    def _constant(self) -> None:
        while self._peek() != '"' and not self._is_at_end():
            self._advance()

        self._advance()

        while self._match('"'):
            pass

        value = self.source[self._start + 1:self._current - 1]
        self._add_token(TokenType.TERMINAL, value)

    def _identifier(self) -> None:
        while self._is_alpha(self._peek()):
            self._advance()

        if token := self._keywords.get(self._current_string):
            if not self._bounded(token):
                self._add_token(token)

            return

        self._add_token(TokenType.IDENTIFIER, self._current_string)

    def _bounded(self, token):
        if _ := token in (TokenType.UNSIGNED, TokenType.UNRESTRICTED):
            self._advance()
            self._scan_token()

        return _

    def _number(self):
        while self._peek().isdigit():
            self._advance()

        self._complex_number()
        self._hex()

        self._add_token(TokenType.NUMBER)

    def _hex(self):
        if self._peek() == 'x':
            self._advance()
            while self._peek() in string.hexdigits:
                self._advance()

    def _complex_number(self):
        for symbol in '.e':
            if self._peek() == symbol:
                self._advance()
                while self._peek().isdigit():
                    self._advance()

    def _advance(self) -> str:
        self._current += 1
        return self.source[self._current - 1]

    def _match(self, expected) -> bool:
        if self._is_at_end() or self.source[self._current] != expected:
            return False

        self._current += 1
        return True

    def _add_token(self, token_type, literal=None) -> None:
        self.tokens.append(
            Token(
                token_type=token_type,
                lexeme=self._current_string,
                literal=literal,
            )
        )

    @property
    def _current_string(self):
        return self.source[self._start:self._current]

    def _peek(self) -> str:
        if self._current >= len(self.source):
            return '\0'

        return self.source[self._current]

    def _is_identifier(self, char: str) -> bool:
        return char in self._identifier_head

    def _is_alpha(self, char: str):
        return char in self._identifier_body

    def _is_at_end(self) -> bool:
        return self._current >= len(self.source)
