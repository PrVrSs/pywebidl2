from typing import Generic, TypeVar

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


_TV = TypeVar('_TV')


class Visitor(Generic[_TV]):
    def visit(self, node: Node) -> _TV:
        return node.accept(self)

    def visit_interface_stmt(self, node: Interface) -> _TV:
        raise NotImplementedError

    def visit_ext_attr(self, node: ExtendedAttribute) -> _TV:
        raise NotImplementedError

    def visit_identifier(self, node: Identifier) -> _TV:
        raise NotImplementedError

    def visit_identifier_list(self, node: IdentifierList) -> _TV:
        raise NotImplementedError

    def visit_operation(self, node: Operation) -> _TV:
        raise NotImplementedError

    def visit_return_type(self, node: ReturnType) -> _TV:
        raise NotImplementedError

    def visit_argument(self, node: Argument) -> _TV:
        raise NotImplementedError

    def visit_argument_type(self, node: ArgumentType) -> _TV:
        raise NotImplementedError
