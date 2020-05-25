from typing import Generic, TypeVar

from .expr import (
    Argument,
    Attribute,
    Callback,
    CallbackInterface,
    Const,
    Constructor,
    Dictionary,
    Enum,
    ExtendedAttribute,
    Field,
    Identifier,
    IdentifierList,
    Includes,
    IdlType,
    Infinity,
    Interface,
    InterfaceMixin,
    Iterable_,
    Literal,
    MapLike,
    Operation,
    Typedef,
    Value,
)

_U = TypeVar('_U')


class Visitor(Generic[_U]):  # pragma: no cover
    # pylint: disable=too-many-public-methods
    def visit(self, expr) -> _U:
        return expr.accept(self)

    def visit_interface(self, node: Interface) -> _U:
        raise NotImplementedError

    def visit_extended_attribute(self, node: ExtendedAttribute) -> _U:
        raise NotImplementedError

    def visit_operation(self, node: Operation) -> _U:
        raise NotImplementedError

    def visit_argument(self, node: Argument) -> _U:
        raise NotImplementedError

    def visit_iterable(self, node: Iterable_) -> _U:
        raise NotImplementedError

    def visit_idl_type(self, node: IdlType) -> _U:
        raise NotImplementedError

    def visit_attribute(self, node: Attribute) -> _U:
        raise NotImplementedError

    def visit_callback(self, node: Callback) -> _U:
        raise NotImplementedError

    def visit_callback_interface(self, node: CallbackInterface) -> _U:
        raise NotImplementedError

    def visit_const(self, node: Const) -> _U:
        raise NotImplementedError

    def visit_identifier(self, node: Identifier) -> _U:
        raise NotImplementedError

    def visit_infinity(self, node: Infinity) -> _U:
        raise NotImplementedError

    def visit_literal(self, node: Literal) -> _U:
        raise NotImplementedError

    def visit_constructor(self, node: Constructor) -> _U:
        raise NotImplementedError

    def visit_dictionary(self, node: Dictionary) -> _U:
        raise NotImplementedError

    def visit_field(self, node: Field) -> _U:
        raise NotImplementedError

    def visit_enum(self, node: Enum) -> _U:
        raise NotImplementedError

    def visit_includes(self, node: Includes) -> _U:
        raise NotImplementedError

    def visit_maplike(self, node: MapLike) -> _U:
        raise NotImplementedError

    def visit_typedef(self, node: Typedef) -> _U:
        raise NotImplementedError

    def visit_interface_mixin(self, node: InterfaceMixin) -> _U:
        raise NotImplementedError

    def visit_identifier_list(self, node: IdentifierList) -> _U:
        raise NotImplementedError

    def visit_value(self, node: Value) -> _U:
        raise NotImplementedError
