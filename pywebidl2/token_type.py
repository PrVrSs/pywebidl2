from enum import IntEnum, auto


class TokenType(IntEnum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_SQUARE = auto()
    RIGHT_SQUARE = auto()
    SEMICOLON = auto()
    DOT = auto()
    EQUAL = auto()
    NEW_LINE = auto()
    WHITESPACE = auto()
    COMMA = auto()
    IDENTIFIER = auto()

    # literals
    TERMINAL = auto()
    NONTERMINAL = auto()

    EOF = auto()
