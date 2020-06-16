from operator import attrgetter
from typing import Generic, TypeVar

import stringcase
from attr import fields

from .expr import (
    Argument,
    AST,
    Attribute,
    Callback,
    CallbackInterface,
    Const,
    Constructor,
    Definitions,
    Dictionary,
    Enum,
    ExtendedAttribute,
    Field,
    Includes,
    IdlType,
    Infinity,
    Interface,
    InterfaceMixin,
    Iterable_,
    Literal,
    LiteralList,
    MapLike,
    Namespace,
    NaN,
    Null,
    Operation,
    SetLike,
    Typedef,
    Value,
)

_U = TypeVar('_U')


class AbcVisitor(Generic[_U]):
    # pylint: disable=too-many-public-methods
    def visit(self, node: AST) -> _U:
        raise NotImplementedError

    def visit_definitions(self, node: Definitions) -> _U:
        raise NotImplementedError

    def visit_interface(self, node: Interface) -> _U:
        raise NotImplementedError

    def visit_interface_mixin(self, node: InterfaceMixin) -> _U:
        raise NotImplementedError

    def visit_callback(self, node: Callback) -> _U:
        raise NotImplementedError

    def visit_callback_interface(self, node: CallbackInterface) -> _U:
        raise NotImplementedError

    def visit_enum(self, node: Enum) -> _U:
        raise NotImplementedError

    def visit_includes(self, node: Includes) -> _U:
        raise NotImplementedError

    def visit_typedef(self, node: Typedef) -> _U:
        raise NotImplementedError

    def visit_namespace(self, node: Namespace) -> _U:
        raise NotImplementedError

    def visit_dictionary(self, node: Dictionary) -> _U:
        raise NotImplementedError

    def visit_argument(self, node: Argument) -> _U:
        raise NotImplementedError

    def visit_iterable(self, node: Iterable_) -> _U:
        raise NotImplementedError

    def visit_operation(self, node: Operation) -> _U:
        raise NotImplementedError

    def visit_constructor(self, node: Constructor) -> _U:
        raise NotImplementedError

    def visit_setlike(self, node: SetLike) -> _U:
        raise NotImplementedError

    def visit_maplike(self, node: MapLike) -> _U:
        raise NotImplementedError

    def visit_attribute(self, node: Attribute) -> _U:
        raise NotImplementedError

    def visit_field(self, node: Field) -> _U:
        raise NotImplementedError

    def visit_const(self, node: Const) -> _U:
        raise NotImplementedError

    def visit_extended_attribute(self, node: ExtendedAttribute) -> _U:
        raise NotImplementedError

    def visit_idl_type(self, node: IdlType) -> _U:
        raise NotImplementedError

    def visit_literal_list(self, node: LiteralList) -> _U:
        raise NotImplementedError

    def visit_literal(self, node: Literal) -> _U:
        raise NotImplementedError

    def visit_value(self, node: Value) -> _U:
        raise NotImplementedError

    def visit_infinity(self, node: Infinity) -> _U:
        raise NotImplementedError

    def visit_nan(self, node: NaN) -> _U:
        raise NotImplementedError

    def visit_null(self, node: Null) -> _U:
        raise NotImplementedError


class IdlNodeVisitor:

    def visit(self, node: AST):
        method = 'visit_' + stringcase.snakecase(node.__class__.__name__)
        visitor = getattr(self, method, self.generic_visit)

        return visitor(node)

    def generic_visit(self, node):
        get_attr_name = attrgetter('name')

        for name in map(get_attr_name, fields(type(node))):
            field = getattr(node, name)

            if isinstance(field, list):
                for item in field:
                    if isinstance(item, AST):
                        self.visit(item)
            elif isinstance(field, AST):
                self.visit(field)
