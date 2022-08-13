from typing import Any

import attr

from .expr import Ast
from .parser import Parser, SyntaxErrorInfo
from .visitor import Visitor


def validate(data: str) -> list[SyntaxErrorInfo]:
    return Parser(data).validate()


def raw_parse(data: str) -> Ast:
    return Visitor(Parser(data).parse()).run()


def parse(data: str) -> dict[str, Any]:
    return attr.asdict(raw_parse(data))  # type: ignore
