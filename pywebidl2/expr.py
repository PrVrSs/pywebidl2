from dataclasses import dataclass, field
from typing import Union

from .utils import escaped_name


@dataclass(kw_only=True)
class Ast:
    ...


@dataclass(kw_only=True)
class Definition(Ast):
    type: str


@dataclass(kw_only=True)
class Member(Ast):
    ...


@dataclass(kw_only=True)
class Expression(Ast):
    ...


@dataclass(kw_only=True)
class Definitions(Ast):
    definitions: list[Definition] = field(default_factory=list)


@dataclass(kw_only=True)
class Null(Expression):
    type: str = field(default='null')


@dataclass(kw_only=True)
class NaN(Expression):
    type: str = field(default='NaN')


@dataclass(kw_only=True)
class Infinity(Expression):
    negative: bool
    type: str = field(default='Infinity')


@dataclass
class Literal(Expression):
    type: str | None
    value: Union[str, list, dict]

    def __post_init__(self):
        self.value = escaped_name(self.value)


@dataclass(kw_only=True)
class Value(Expression):
    value: str

    def __post_init__(self):
        self.value = escaped_name(self.value)


@dataclass(kw_only=True)
class LiteralList(Expression):
    type: str
    value: list[Value] = field(default_factory=list)


@dataclass(kw_only=True)
class ExtendedAttribute(Ast):
    name: str
    arguments: list[str] = field(default_factory=list)
    rhs: Union[Literal, LiteralList] | None = field(default=None)
    type: str = field(default='extended-attribute')


@dataclass(kw_only=True)
class IdlType(Ast):
    idl_type: Union[list['IdlType'], 'IdlType', str]
    type: str | None = field(default=None)
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)
    nullable: bool = field(default=False)
    union: bool = field(default=False)
    generic: str = field(default='')

    def __post_init__(self):
        self.idl_type = escaped_name(self.idl_type)


@dataclass(kw_only=True)
class Argument(Ast):
    name: str
    idl_type: IdlType
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)
    default: Union[Literal, Value] | None = field(default=None)
    type: str = field(default='argument')
    optional: bool = field(default=False)
    variadic: bool = field(default=False)

    def __post_init__(self):
        self.name = escaped_name(self.name)


@dataclass(kw_only=True)
class Operation(Member):
    name: str
    idl_type: IdlType | None
    arguments: list[Argument] = field(default_factory=list)
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)
    type: str = field(default='operation')
    special: str = field(default='')


@dataclass(kw_only=True)
class Iterable_(Member):  # pylint: disable=invalid-name
    idl_type: list[IdlType]
    arguments: list[Argument]
    async_: bool
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)
    type: str = field(default='iterable')
    readonly: bool = field(default=False)


@dataclass(kw_only=True)
class Attribute(Member):
    idl_type: IdlType
    name: str
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)
    type: str = field(default='attribute')
    readonly: bool = field(default=False)
    special: str = field(default='')

    def __post_init__(self):
        self.name = escaped_name(self.name)


@dataclass(kw_only=True)
class Const(Member):
    name: str
    value: Expression
    idl_type: IdlType
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)
    type: str = field(default='const')


@dataclass(kw_only=True)
class Constructor(Member):
    arguments: list[Argument] = field(default_factory=list)
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)
    type: str = field(default='constructor')


@dataclass
class MapLike(Member):
    readonly: bool
    idl_type: list[IdlType]
    arguments: list[Argument] = field(default_factory=list)
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)
    type: str = field(default='maplike')
    async_: bool = field(default=False)


@dataclass(kw_only=True)
class SetLike(Member):
    readonly: bool
    idl_type: list[IdlType]
    arguments: list[Argument] = field(default_factory=list)
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)
    type: str = field(default='setlike')
    async_: bool = field(default=False)


@dataclass(kw_only=True)
class Field(Member):
    idl_type: IdlType
    name: str
    default: Literal | None
    required: bool = field(default=False)
    type: str = field(default='field')
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)


@dataclass(kw_only=True)
class CallbackInterface(Definition):
    name: str
    members: list[Member]
    inheritance: str | None
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)
    type: str = field(default='callback interface')
    partial: bool = field(default=False)


@dataclass(kw_only=True)
class Callback(Definition):
    name: str
    idl_type: IdlType
    arguments: list[Argument] = field(default_factory=list)
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)
    type: str = field(default='callback')


@dataclass(kw_only=True)
class Interface(Definition):
    members: list[Member]
    name: str
    inheritance: str | None = field(default=None)
    partial: bool = field(default=False)
    type: str = field(default='interface')
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)

    def __post_init__(self):
        self.name = escaped_name(self.name)
        self.inheritance = escaped_name(self.inheritance)


@dataclass(kw_only=True)
class InterfaceMixin(Definition):
    members: list[Member]
    name: str
    inheritance: str | None = field(default=None)
    partial: bool = field(default=False)
    type: str = field(default='interface mixin')
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)

    def __post_init__(self):
        self.name = escaped_name(self.name)
        self.inheritance = escaped_name(self.inheritance)


@dataclass(kw_only=True)
class Enum(Definition):
    name: str
    type: str = field(default='enum')
    values: list[Literal] = field(default_factory=list)
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)


@dataclass(kw_only=True)
class Dictionary(Definition):
    name: str
    inheritance: str | None = field(default=None)
    members: list[Member] = field(default_factory=list)
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)
    type: str = field(default='dictionary')
    partial: bool = field(default=False)

    def __post_init__(self):
        self.name = escaped_name(self.name)


@dataclass(kw_only=True)
class Includes(Definition):
    target: str
    includes: str
    type: str = field(default='includes')
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)

    def __post_init__(self):
        self.target = escaped_name(self.target)
        self.includes = escaped_name(self.includes)


@dataclass(kw_only=True)
class Typedef(Definition):
    idl_type: IdlType
    name: str
    type: str = field(default='typedef')
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)

    def __post_init__(self):
        self.name = escaped_name(self.name)


@dataclass(kw_only=True)
class Namespace(Definition):
    members: list[Member]
    name: str
    inheritance: str | None = field(default=None)
    partial: bool = field(default=False)
    type: str = field(default='namespace')
    ext_attrs: list[ExtendedAttribute] = field(default_factory=list)

    def __post_init__(self):
        self.name = escaped_name(self.name)
