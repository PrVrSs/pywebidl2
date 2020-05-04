from collections import deque

from .expressions import Expression
from .statement import Statement


def iter_fields(node):
    for field in node._fields:
        try:
            yield field, getattr(node, field)
        except AttributeError:
            pass


def iter_child_nodes(node):
    for name, field in iter_fields(node):
        if isinstance(field, (Expression, Statement)):
            yield field
        elif isinstance(field, list):
            for item in field:
                if isinstance(item, (Expression, Statement)):
                    yield item


def walk(node):
    todo = deque([node])

    while todo:
        node = todo.popleft()
        todo.extend(iter_child_nodes(node))
        yield node
