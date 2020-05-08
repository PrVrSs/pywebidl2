from enum import IntEnum, auto


class TokenType(IntEnum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_SQUARE = auto()
    RIGHT_SQUARE = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_ANGLE = auto()
    RIGHT_ANGLE = auto()
    SEMICOLON = auto()
    DOT = auto()
    EQUAL = auto()
    NEW_LINE = auto()
    WHITESPACE = auto()
    COMMA = auto()
    IDENTIFIER = auto()

    ASYNC = auto()
    ITERABLE = auto()
    OPTIONAL = auto()
    INTERFACE = auto()

    # literals
    TERMINAL = auto()
    NONTERMINAL = auto()

    EOF = auto()
