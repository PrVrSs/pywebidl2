from typing import Generic, TypeVar

from .node import (
    Node,
    Argument,
    Attribute,
    ExtendedAttribute,
    Identifier,
    IdentifierList,
    IDLType,
    Iterable_,
    Interface,
    Operation,
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

    def visit_argument(self, node: Argument) -> _TV:
        raise NotImplementedError

    def visit_iterable(self, node: Iterable_) -> _TV:
        raise NotImplementedError

    def visit_idl_type(self, node: IDLType) -> _TV:
        raise NotImplementedError

    def visit_attribute(self, node: Attribute) -> _TV:
        raise NotImplementedError
