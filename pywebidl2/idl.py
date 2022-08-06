from typing import Any

import attr

from .expr import Ast
from .parser import Parser, SyntaxErrorInfo
from .visitor import Visitor


def validate(file: str) -> list[SyntaxErrorInfo]:
    return Parser(file).validate()


def parse(file: str) -> Ast:
    return Visitor(Parser(file).parse()).run()


def parse_as_dict(file: str) -> dict[str, Any]:
    return attr.asdict(parse(file))  # type: ignore
