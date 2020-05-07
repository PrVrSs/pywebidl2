from typing import Iterable

# TODO: add `as_dict method`
# TODO: use metaclass - remove boilerplate. or just attrs


class Node:

    type: str

    @property
    def children(self) -> Iterable['Node']:
        for field in vars(self).values():
            if isinstance(field, Node):
                yield field
            elif isinstance(field, list):
                for item in field:
                    if isinstance(item, Node):
                        yield item

    def accept(self, visitor):
        raise NotImplementedError


class Interface(Node):

    type = 'interface'

    def __init__(
            self,
            name,
            inheritance=None,
            partial=False,
            members=None,
            ext_attrs=None,
    ):
        self.name = name
        self.inheritance = inheritance
        self.members = members or []
        self.ext_attrs = ext_attrs or []
        self.partial = partial

    def accept(self, visitor):
        return visitor.visit_interface_stmt(self)


class ExtendedAttribute(Node):

    type = 'extended-attribute'

    def __init__(self, name, rhs=None, arguments=None):
        self.name = name
        self.rhs = rhs or []
        self.arguments = arguments or []

    def accept(self, visitor):
        return visitor.visit_ext_attr(self)


class Operation(Node):

    type = 'operation'

    def __init__(self, name, idl_type=None, arguments=None, ext_attrs=None, special=''):
        self.name = name
        self.idl_type = idl_type
        self.arguments = arguments or []
        self.ext_attrs = ext_attrs or []
        self.special = special

    def accept(self, visitor):
        return visitor.visit_operation(self)


class ReturnType(Node):

    type = 'return-type'

    def __init__(
            self,
            idl_type,
            nullable=False,
            union=False,
            ext_attrs=None,
            generic='',
    ):
        self.idl_type = idl_type
        self.nullable = nullable
        self.union = union
        self.ext_attrs = ext_attrs or []
        self.generic = generic

    def accept(self, visitor):
        return visitor.visit_return_type(self)


class Argument(Node):

    type = 'argument'

    def __init__(self, name, idl_type, ext_attrs=None, default=None, optional=False, variadic=False):
        self.name = name
        self.ext_attrs = ext_attrs or []
        self.idl_type = idl_type
        self.default = default
        self.optional = optional
        self.variadic = variadic

    def accept(self, visitor):
        return visitor.visit_argument(self)


class ArgumentType(Node):

    type = 'argument-type'

    def __init__(
            self,
            idl_type,
            nullable=False,
            union=False,
            ext_attrs=None,
            generic='',
    ):
        self.idl_type = idl_type
        self.nullable = nullable
        self.union = union
        self.ext_attrs = ext_attrs or []
        self.generic = generic

    def accept(self, visitor):
        return visitor.visit_argument_type(self)


class Identifier(Node):

    type = 'identifier'

    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_identifier(self)


class IdentifierList(Node):

    type = 'identifier-list'

    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_identifier_list(self)
