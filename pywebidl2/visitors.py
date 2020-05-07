from typing import Iterable

from .productions import Visitor
from .productions.node import (
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


class Walker(Visitor):

    def _visit_children(self, node: Node) -> Iterable[Node]:
        yield node

        for child in node.children:
            yield from child.accept(self)

    def visit_interface_stmt(self, node: Interface) -> Iterable[Node]:
        return self._visit_children(node)

    def visit_ext_attr(self, node: ExtendedAttribute) -> Iterable[Node]:
        return self._visit_children(node)

    def visit_identifier(self, node: Identifier) -> Iterable[Node]:
        return self._visit_children(node)

    def visit_identifier_list(self, node: IdentifierList) -> Iterable[Node]:
        return self._visit_children(node)

    def visit_operation(self, node: Operation) -> Iterable[Node]:
        return self._visit_children(node)

    def visit_return_type(self, node: ReturnType) -> Iterable[Node]:
        return self._visit_children(node)

    def visit_argument(self, node: Argument) -> Iterable[Node]:
        return self._visit_children(node)

    def visit_argument_type(self, node: ArgumentType) -> Iterable[Node]:
        return self._visit_children(node)


class JsonView(Visitor):

    def visit_interface_stmt(self, node):
        return dict(
            type=node.type,
            name=node.name.lexeme,
            extAttrs=[ext_attr.accept(self) for ext_attr in node.ext_attrs],
            members=[member.accept(self) for member in node.members],
            inheritance=node.inheritance,
            partial=node.partial,
        )

    def visit_operation(self, node):
        return dict(
            type=node.type,
            name=node.name.lexeme,
            idlType=node.idl_type.accept(self),
            arguments=[argument.accept(self) for argument in node.arguments],
            special=node.special,
            extAttrs=[ext_attr.accept(self) for ext_attr in node.ext_attrs],
        )

    def visit_argument(self, node):
        return dict(
            name=node.name.lexeme,
            type=node.type,
            idlType=node.idl_type.accept(self),
            default=node.default,
            optional=node.optional,
            variadic=node.variadic,
            extAttrs=[ext_attr.accept(self) for ext_attr in node.ext_attrs],
        )

    def visit_argument_type(self, node):
        return dict(
            type=node.type,
            idlType=node.idl_type.lexeme,
            nullable=node.nullable,
            union=node.union,
            extAttrs=[ext_attr.accept(self) for ext_attr in node.ext_attrs],
            generic=node.generic,
        )

    def visit_return_type(self, node):
        return dict(
            type=node.type,
            idlType=node.idl_type.lexeme,
            nullable=node.nullable,
            union=node.union,
            extAttrs=[ext_attr.accept(self) for ext_attr in node.ext_attrs],
            generic=node.generic,
        )

    def visit_ext_attr(self, node):
        return dict(
            type=node.type,
            name=node.name.lexeme,
            rhs=node.rhs and node.rhs.accept(self) or None,
            arguments=[argument.accept(self) for argument in node.arguments],
        )

    def visit_identifier(self, node):
        return dict(
            type=node.type,
            value=node.value.lexeme,
        )

    def visit_identifier_list(self, node):
        return dict(
            type=node.type,
            value=[{'value': value} for value in node.value],
        )
