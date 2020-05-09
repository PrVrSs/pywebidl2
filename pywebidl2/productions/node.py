import logging
from typing import Any, List, Iterable

from .tokeniser import Token


__all__ = (
    'Node',
    'Argument',
    'Attribute',
    'ExtendedAttribute',
    'Identifier',
    'IdentifierList',
    'IDLType',
    'Interface',
    'Iterable_',
    'Operation',
)


class NodeMeta(type):
    def __new__(mcs, typename, bases, ns):
        if not bases:
            return super().__new__(mcs, typename, bases, ns)

        ns['__init__'] = mcs._init_

        return super().__new__(mcs, typename, bases, ns)

    @staticmethod
    def _init_(__obj__, **kwargs):
        for name, value in kwargs.items():
            if name in __obj__.__annotations__:
                setattr(__obj__, name, value)
            else:
                logging.debug('Discarded %s', name)


class Node(metaclass=NodeMeta):

    def __init__(self, **_):
        ...

    @property
    def children(self) -> Iterable['Node']:
        for field_name in self.__annotations__.keys():
            field = getattr(self, field_name, None)

            if isinstance(field, Node):
                yield field
            elif isinstance(field, list):
                for item in field:
                    if isinstance(item, Node):
                        yield item

    def accept(self, visitor):
        raise NotImplementedError


class Interface(Node):

    name: Token
    members: List[Any]
    ext_attrs: List[Any]

    type: str = 'interface'
    inheritance: Any = None
    partial: bool = False

    def accept(self, visitor):
        return visitor.visit_interface_stmt(self)


class ExtendedAttribute(Node):

    name: Token
    rhs: List[Any]
    arguments: List[Any]

    type: str = 'extended-attribute'

    def accept(self, visitor):
        return visitor.visit_ext_attr(self)


class Operation(Node):

    name: Token
    arguments: List[Any]
    ext_attrs: List[Any]

    type: str = 'operation'
    special: str = ''
    idl_type: Any = None

    def accept(self, visitor):
        return visitor.visit_operation(self)


class Argument(Node):

    name: Token
    ext_attrs: List[Any]
    idl_type: Any

    default: Any = None
    type: str = 'argument'
    optional: bool = False
    variadic: bool = False

    def accept(self, visitor):
        return visitor.visit_argument(self)


class Identifier(Node):

    value: Any

    type: str = 'identifier'

    def accept(self, visitor):
        return visitor.visit_identifier(self)


class IdentifierList(Node):

    value: Any

    type: str = 'identifier-list'

    def accept(self, visitor):
        return visitor.visit_identifier_list(self)


class Iterable_(Node):  # pylint: disable=invalid-name

    idl_type: List[Any]
    arguments: List[Any]
    ext_attrs: List[Any]

    type: str = 'iterable'
    async_: bool = False
    readonly: bool = False

    def accept(self, visitor):
        return visitor.visit_iterable(self)


class Attribute(Node):

    name: Token
    ext_attrs: List[Any]

    type: str = 'attribute'
    readonly: bool = False
    idl_type: Any = None
    special: str = ''

    def accept(self, visitor):
        return visitor.visit_attribute(self)


class IDLType(Node):

    ext_attrs: List[Any]
    idl_type: Any

    type: Any = None
    generic: str = ''
    union: bool = False
    nullable: bool = False

    def accept(self, visitor):
        return visitor.visit_idl_type(self)
