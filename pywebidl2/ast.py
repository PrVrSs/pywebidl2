from typing import List

from .node import (
    Node,
    Argument,
    ArgumentType,
    ExtendedAttribute,
    Identifier,
    IdentifierList,
    Interface,
    Operation,
    ReturnType,
)
from .visitor import Visitor


class walk(Visitor):

    def __new__(cls, node: Node) -> List[Node]:
        return super().__new__(cls).visit(node)

    def _visit_children(self, node: Node) -> List[Node]:
        yield node

        for child in node.children:
            yield from child.accept(self)

    def visit_interface_stmt(self, node: Interface) -> List[Node]:
        return self._visit_children(node)

    def visit_ext_attr(self, node: ExtendedAttribute) -> List[Node]:
        return self._visit_children(node)

    def visit_identifier(self, node: Identifier) -> List[Node]:
        return self._visit_children(node)

    def visit_identifier_list(self, node: IdentifierList) -> List[Node]:
        return self._visit_children(node)

    def visit_operation(self, node: Operation) -> List[Node]:
        return self._visit_children(node)

    def visit_return_type(self, node: ReturnType) -> List[Node]:
        return self._visit_children(node)

    def visit_argument(self, node: Argument) -> List[Node]:
        return self._visit_children(node)

    def visit_argument_type(self, node: ArgumentType) -> List[Node]:
        return self._visit_children(node)
