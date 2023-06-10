from collections import deque
from contextlib import suppress
from typing import Any, TypeVar


_U = TypeVar('_U')


def setup_type(idl_type: Any, type_: str) -> None:
    todo = deque([idl_type])

    with suppress(IndexError):
        while idl_type := todo.popleft():
            idl_type.type = type_

            if idl_type.generic:
                todo.extend(idl_type.idl_type)


def escaped_name(string: _U | str) -> _U | str:
    if isinstance(string, str):
        return string.lstrip('_')

    return string
