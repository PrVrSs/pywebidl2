from collections import deque
from contextlib import suppress
from typing import Any


def setup_type(idl_type, type_):
    todo = deque([idl_type])

    with suppress(IndexError):
        while idl_type := todo.popleft():
            idl_type.type = type_

            if idl_type.generic:
                todo.extend(idl_type.idl_type)


def escaped_name(string: Any) -> Any:
    if isinstance(string, str):
        return string.lstrip('_')

    return string
