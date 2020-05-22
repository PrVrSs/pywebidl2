from typing import Any


def escaped_name(string: Any) -> Any:
    if isinstance(string, str):
        return string.lstrip('_')

    return string
