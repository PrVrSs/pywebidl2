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
    IdlType,
    Infinity,
    Interface,
    Iterable_,
    Literal,
    Operation,
    Value,
)

_TV = TypeVar('_TV')


class Visitor(Generic[_TV]):  # pragma: no cover
    def visit(self, expr) -> _TV:
        return expr.accept(self)

    def visit_interface(self, node: Interface) -> _TV:
        raise NotImplementedError

    def visit_ext_attr(self, node: ExtendedAttribute) -> _TV:
        raise NotImplementedError

    # def visit_identifier(self, node: Identifier) -> _TV:
    #     raise NotImplementedError
    #
    # def visit_identifier_list(self, node: IdentifierList) -> _TV:
    #     raise NotImplementedError

    def visit_operation(self, node: Operation) -> _TV:
        raise NotImplementedError

    def visit_argument(self, node: Argument) -> _TV:
        raise NotImplementedError

    def visit_iterable(self, node: Iterable_) -> _TV:
        raise NotImplementedError

    def visit_idl_type(self, node: IdlType) -> _TV:
        raise NotImplementedError

    def visit_attribute(self, node: Attribute) -> _TV:
        raise NotImplementedError

    def visit_callback(self, node: Callback) -> _TV:
        raise NotImplementedError

    def visit_callback_interface(self, node: CallbackInterface) -> _TV:
        raise NotImplementedError

    def visit_const(self, node: Const) -> _TV:
        raise NotImplementedError

    def visit_value(self, node: Value) -> _TV:
        raise NotImplementedError

    def visit_infinity(self, node: Infinity) -> _TV:
        raise NotImplementedError

    def visit_literal(self, node: Literal) -> _TV:
        raise NotImplementedError

    def visit_constructor(self, node: Constructor) -> _TV:
        raise NotImplementedError

    def visit_dictionary(self, node: Dictionary) -> _TV:
        raise NotImplementedError

    def visit_field(self, node: Field) -> _TV:
        raise NotImplementedError

    def visit_enum(self, node: Enum) -> _TV:
        raise NotImplementedError
