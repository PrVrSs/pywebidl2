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
    COMMA = auto()
    MINUS = auto()
    PLUS = auto()
    NEW_LINE = auto()
    WHITESPACE = auto()

    NAN = auto()
    FALSE = auto()
    TRUE = auto()
    UNRESTRICTED = auto()
    INFINITY = auto()
    CONST = auto()
    CALLBACK = auto()
    UNSIGNED = auto()
    ASYNC = auto()
    ATTRIBUTE = auto()
    ITERABLE = auto()
    OPTIONAL = auto()
    INTERFACE = auto()

    NUMBER = auto()
    IDENTIFIER = auto()

    TERMINAL = auto()
    NONTERMINAL = auto()

    EOF = auto()
