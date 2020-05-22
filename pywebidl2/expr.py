from typing import Any, List, Optional

import attr

from .utils import escaped_name


@attr.s
class Interface:

    members: List[Any] = attr.ib()
    name: str = attr.ib(converter=escaped_name)
    partial: bool = attr.ib()
    inheritance: Optional[str] = attr.ib(converter=escaped_name)
    type: str = attr.ib(default='interface')
    ext_attrs: List[Any] = attr.ib(default=attr.Factory(list))

    def accept(self, visitor):
        visitor.visit_interface(self)


@attr.s
class Enum:

    name: str = attr.ib()
    type: str = attr.ib(default='enum')
    values: List[Any] = attr.ib(default=attr.Factory(list))
    ext_attrs: List[Any] = attr.ib(default=attr.Factory(list))

    def accept(self, visitor):
        visitor.visit_enum(self)


@attr.s
class IdlType:

    idl_type: Any = attr.ib(converter=escaped_name)
    type: Optional[str] = attr.ib(default=None)
    ext_attrs: List[Any] = attr.ib(default=attr.Factory(list))
    nullable: bool = attr.ib(default=False)
    union: bool = attr.ib(default=False)
    generic: str = attr.ib(default='')

    def accept(self, visitor):
        visitor.visit_idl_type(self)


@attr.s
class Operation:

    name: str = attr.ib()
    idl_type: IdlType = attr.ib()

    arguments = attr.ib(default=attr.Factory(list))
    ext_attrs = attr.ib(default=attr.Factory(list))
    type: str = attr.ib(default='operation')
    special: str = attr.ib(default='')

    def accept(self, visitor):
        visitor.visit_operation(self)


@attr.s
class Argument:

    name = attr.ib()
    idl_type = attr.ib()
    ext_attrs = attr.ib()

    default = attr.ib(default=None)
    type: str = attr.ib(default='argument')
    optional: bool = attr.ib(default=False)
    variadic: bool = attr.ib(default=False)

    def accept(self, visitor):
        visitor.visit_argument(self)


@attr.s
class ExtendedAttribute:

    name: str = attr.ib()

    arguments = attr.ib(default=attr.Factory(list))
    rhs = attr.ib(default=None)
    type: str = attr.ib(default='extended-attribute')

    def accept(self, visitor):
        return visitor.visit_ext_attr(self)


@attr.s
class Iterable_:  # pylint: disable=invalid-name

    idl_type = attr.ib()
    arguments = attr.ib()
    ext_attrs = attr.ib()

    type: str = attr.ib(default='iterable')
    async_: bool = attr.ib(default=False)
    readonly: bool = attr.ib(default=False)

    def accept(self, visitor):
        return visitor.visit_iterable(self)


@attr.s
class Attribute:

    name = attr.ib()
    idl_type = attr.ib()

    ext_attrs = attr.ib(default=attr.Factory(list))
    type: str = attr.ib(default='attribute')
    readonly: bool = attr.ib(default=False)
    special: str = attr.ib(default='')

    def accept(self, visitor):
        return visitor.visit_attribute(self)


@attr.s
class CallbackInterface:

    name = attr.ib()
    members = attr.ib()
    inheritance = attr.ib()

    ext_attrs = attr.ib(default=attr.Factory(list))
    type: str = attr.ib(default='callback interface')
    partial: bool = attr.ib(default=False)

    def accept(self, visitor):
        return visitor.visit_callback_interface(self)


@attr.s
class Callback:

    name = attr.ib()
    idl_type = attr.ib()
    arguments = attr.ib()
    ext_attrs = attr.ib(default=attr.Factory(list))

    type: str = attr.ib(default='callback')

    def accept(self, visitor):
        return visitor.visit_callback(self)


@attr.s
class Const:

    name = attr.ib()
    value = attr.ib()
    idl_type = attr.ib()

    ext_attrs = attr.ib(default=attr.Factory(list))
    type: str = attr.ib(default='const')

    def accept(self, visitor):
        return visitor.visit_const(self)


@attr.s
class Value:

    type = attr.ib()
    value = attr.ib()

    def accept(self, visitor):
        return visitor.visit_value(self)


@attr.s
class Infinity:

    negative: bool = attr.ib()
    type: str = attr.ib(default='Infinity')

    def accept(self, visitor):
        return visitor.visit_infinity(self)


@attr.s
class Literal:

    type: str = attr.ib()

    def accept(self, visitor):
        return visitor.visit_literal(self)


@attr.s
class Constructor:

    arguments = attr.ib(default=attr.Factory(list))
    ext_attrs = attr.ib(default=attr.Factory(list))
    type: str = attr.ib(default='constructor')

    def accept(self, visitor):
        return visitor.visit_constructor(self)


@attr.s
class Dictionary:

    name = attr.ib()

    inheritance = attr.ib(default=None)
    members = attr.ib(default=attr.Factory(list))
    ext_attrs = attr.ib(default=attr.Factory(list))
    type: str = attr.ib(default='dictionary')
    partial = attr.ib(default=False)

    def accept(self, visitor):
        return visitor.visit_dictionary(self)


@attr.s
class Field:

    idl_type = attr.ib()
    name = attr.ib()
    default = attr.ib()
    required: bool = attr.ib(default=False)
    type: str = attr.ib(default='field')
    ext_attrs = attr.ib(default=attr.Factory(list))

    def accept(self, visitor):
        return visitor.visit_field(self)


@attr.s
class Includes:

    target: str = attr.ib(converter=escaped_name)
    includes: str = attr.ib(converter=escaped_name)
    type: str = attr.ib(default='includes')
    ext_attrs: List[Any] = attr.ib(default=attr.Factory(list))

    def accept(self, visitor):
        return visitor.visit_includes(self)


@attr.s
class Typedef:

    idl_type: Any = attr.ib()
    name: str = attr.ib()
    type: str = attr.ib(default='typedef')
    ext_attrs: List[Any] = attr.ib(default=attr.Factory(list))

    def accept(self, visitor):
        return visitor.visit_typedef(self)
