import abc
from typing import List, Optional, Union

import attr

from .utils import escaped_name


class AST(abc.ABC):

    @abc.abstractmethod
    def accept(self, visitor):
        ...


class Definition(AST):

    @abc.abstractmethod
    def accept(self, visitor):
        ...


class Member(AST):

    @abc.abstractmethod
    def accept(self, visitor):
        ...


class Expression(AST):

    @abc.abstractmethod
    def accept(self, visitor):
        ...


@attr.s
class Definitions(Definition):

    definitions: List[Definition] = attr.ib(factory=list)

    def accept(self, visitor):
        visitor.visit_definitions(self)


@attr.s
class Null(Expression):

    type: str = attr.ib(default='null')

    def accept(self, visitor):
        return visitor.visit_null(self)


@attr.s
class NaN(Expression):

    type: str = attr.ib(default='NaN')

    def accept(self, visitor):
        return visitor.visit_nan(self)


@attr.s
class Infinity(Expression):

    negative: bool = attr.ib()
    type: str = attr.ib(default='Infinity')

    def accept(self, visitor):
        return visitor.visit_infinity(self)


@attr.s
class Literal(Expression):

    type: Optional[str] = attr.ib()
    value: Union[str, list] = attr.ib()

    def __attrs_post_init__(self):
        self.value = escaped_name(self.value)

    def accept(self, visitor):
        return visitor.visit_literal(self)


@attr.s
class Value(Expression):

    value: str = attr.ib()

    def __attrs_post_init__(self):
        self.value = escaped_name(self.value)

    def accept(self, visitor):
        return visitor.visit_value(self)


@attr.s
class LiteralList(Expression):

    type: str = attr.ib()
    value: List[Value] = attr.ib(factory=list)

    def accept(self, visitor):
        return visitor.visit_literal_list(self)


@attr.s
class ExtendedAttribute(AST):

    name: str = attr.ib()
    arguments: List[str] = attr.ib(factory=list)
    rhs: Optional[Union[Literal, LiteralList]] = attr.ib(default=None)
    type: str = attr.ib(default='extended-attribute')

    def accept(self, visitor):
        return visitor.visit_extended_attribute(self)


@attr.s
class IdlType(AST):

    idl_type: Union[List['IdlType'], 'IdlType', str] = attr.ib()
    type: Optional[str] = attr.ib(default=None)
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)
    nullable: bool = attr.ib(default=False)
    union: bool = attr.ib(default=False)
    generic: str = attr.ib(default='')

    def __attrs_post_init__(self):
        self.idl_type = escaped_name(self.idl_type)

    def accept(self, visitor):
        return visitor.visit_idl_type(self)


@attr.s
class Argument(AST):

    name: str = attr.ib()
    idl_type: IdlType = attr.ib()
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)
    default: Optional[Union[Literal, Value]] = attr.ib(default=None)
    type: str = attr.ib(default='argument')
    optional: bool = attr.ib(default=False)
    variadic: bool = attr.ib(default=False)

    def __attrs_post_init__(self):
        self.name = escaped_name(self.name)

    def accept(self, visitor):
        return visitor.visit_argument(self)


@attr.s
class Operation(Member):

    name: str = attr.ib()
    idl_type: Optional[IdlType] = attr.ib()
    arguments: List[Argument] = attr.ib(factory=list)
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)
    type: str = attr.ib(default='operation')
    special: str = attr.ib(default='')

    def accept(self, visitor):
        return visitor.visit_operation(self)


@attr.s
class Iterable_(Member):  # pylint: disable=invalid-name

    idl_type: List[IdlType] = attr.ib()
    arguments: List[Argument] = attr.ib()
    async_: bool = attr.ib()
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)
    type: str = attr.ib(default='iterable')
    readonly: bool = attr.ib(default=False)

    def accept(self, visitor):
        return visitor.visit_iterable(self)


@attr.s
class Attribute(Member):

    idl_type: IdlType = attr.ib()
    name: str = attr.ib()
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)
    type: str = attr.ib(default='attribute')
    readonly: bool = attr.ib(default=False)
    special: str = attr.ib(default='')

    def __attrs_post_init__(self):
        self.name = escaped_name(self.name)

    def accept(self, visitor):
        return visitor.visit_attribute(self)


@attr.s
class Const(Member):

    name: str = attr.ib()
    value: Expression = attr.ib()
    idl_type: IdlType = attr.ib()
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)
    type: str = attr.ib(default='const')

    def accept(self, visitor):
        return visitor.visit_const(self)


@attr.s
class Constructor(Member):

    arguments: List[Argument] = attr.ib(factory=list)
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)
    type: str = attr.ib(default='constructor')

    def accept(self, visitor):
        return visitor.visit_constructor(self)


@attr.s
class MapLike(Member):

    readonly: bool = attr.ib()
    idl_type: List[IdlType] = attr.ib()
    arguments: List[Argument] = attr.ib(factory=list)
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)
    type: str = attr.ib(default='maplike')
    async_: bool = attr.ib(default=False)

    def accept(self, visitor):
        return visitor.visit_maplike(self)


@attr.s
class SetLike(Member):

    readonly: bool = attr.ib()
    idl_type: List[IdlType] = attr.ib()
    arguments: List[Argument] = attr.ib(factory=list)
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)
    type: str = attr.ib(default='setlike')
    async_: bool = attr.ib(default=False)

    def accept(self, visitor):
        return visitor.visit_setlike(self)


@attr.s
class Field(Member):

    idl_type: IdlType = attr.ib()
    name: str = attr.ib()
    default: Optional[Literal] = attr.ib()
    required: bool = attr.ib(default=False)
    type: str = attr.ib(default='field')
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)

    def accept(self, visitor):
        return visitor.visit_field(self)


@attr.s
class CallbackInterface(Definition):

    name: str = attr.ib()
    members: List[Member] = attr.ib()
    inheritance: Optional[str] = attr.ib()
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)
    type: str = attr.ib(default='callback interface')
    partial: bool = attr.ib(default=False)

    def accept(self, visitor):
        return visitor.visit_callback_interface(self)


@attr.s
class Callback(Definition):

    name: str = attr.ib()
    idl_type: IdlType = attr.ib()
    arguments: List[Argument] = attr.ib(factory=list)
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)
    type: str = attr.ib(default='callback')

    def accept(self, visitor):
        return visitor.visit_callback(self)


@attr.s
class Interface(Definition):

    members: List[Member] = attr.ib()
    name: str = attr.ib()
    inheritance: Optional[str] = attr.ib(default=None)
    partial: bool = attr.ib(default=False)
    type: str = attr.ib(default='interface')
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)

    def __attrs_post_init__(self):
        self.name = escaped_name(self.name)
        self.inheritance = escaped_name(self.inheritance)

    def accept(self, visitor):
        return visitor.visit_interface(self)


@attr.s
class InterfaceMixin(Definition):

    members: List[Member] = attr.ib()
    name: str = attr.ib()
    inheritance: Optional[str] = attr.ib(default=None)
    partial: bool = attr.ib(default=False)
    type: str = attr.ib(default='interface mixin')
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)

    def __attrs_post_init__(self):
        self.name = escaped_name(self.name)
        self.inheritance = escaped_name(self.inheritance)

    def accept(self, visitor):
        return visitor.visit_interface_mixin(self)


@attr.s
class Enum(Definition):

    name: str = attr.ib()
    type: str = attr.ib(default='enum')
    values: List[Literal] = attr.ib(factory=list)
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)

    def accept(self, visitor):
        return visitor.visit_enum(self)


@attr.s
class Dictionary(Definition):

    name: str = attr.ib()
    inheritance: Optional[str] = attr.ib(default=None)
    members: List[Member] = attr.ib(factory=list)
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)
    type: str = attr.ib(default='dictionary')
    partial: bool = attr.ib(default=False)

    def __attrs_post_init__(self):
        self.name = escaped_name(self.name)

    def accept(self, visitor):
        return visitor.visit_dictionary(self)


@attr.s
class Includes(Definition):

    target: str = attr.ib()
    includes: str = attr.ib()
    type: str = attr.ib(default='includes')
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)

    def __attrs_post_init__(self):
        self.target = escaped_name(self.target)
        self.includes = escaped_name(self.includes)

    def accept(self, visitor):
        return visitor.visit_includes(self)


@attr.s
class Typedef(Definition):

    idl_type: IdlType = attr.ib()
    name: str = attr.ib()
    type: str = attr.ib(default='typedef')
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)

    def __attrs_post_init__(self):
        self.name = escaped_name(self.name)

    def accept(self, visitor):
        return visitor.visit_typedef(self)


@attr.s
class Namespace(Definition):

    members: List[Member] = attr.ib()
    name: str = attr.ib()
    inheritance: Optional[str] = attr.ib(default=None)
    partial: bool = attr.ib(default=False)
    type: str = attr.ib(default='namespace')
    ext_attrs: List[ExtendedAttribute] = attr.ib(factory=list)

    def __attrs_post_init__(self):
        self.name = escaped_name(self.name)

    def accept(self, visitor):
        return visitor.visit_namespace(self)
