# TODO: add `as_dict method`
# TODO: use metaclass - remove boilerplate. or just attrs


class Statement:
    type: str
    _fields: tuple


class Partial(Statement):

    type = 'partial'

    def __init__(self):
        pass

    def accept(self, visitor):
        return visitor.visit_partial_stmt(self)


class Interface(Statement):

    type = 'interface'

    _fields = (
        'name',
        'inheritance',
        'members',
        'ext_attrs',
        'partial',
    )

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


class ExtendedAttribute(Statement):

    type = 'extended-attribute'

    _fields = (
        'name',
        'rhs',
        'arguments',
    )

    def __init__(self, name, rhs=None, arguments=None):
        self.name = name
        self.rhs = rhs or []
        self.arguments = arguments or []

    def accept(self, visitor):
        return visitor.visit_ext_attr(self)


class Operation(Statement):
    type = 'operation'

    _fields = (
        'name',
        'idl_type',
        'arguments',
        'ext_attrs',
        'special',
    )

    def __init__(self, name, idl_type=None, arguments=None, ext_attrs=None, special=''):
        self.name = name
        self.idl_type = idl_type
        self.arguments = arguments or []
        self.ext_attrs = ext_attrs or []
        self.special = special

    def accept(self, visitor):
        return visitor.visit_operation(self)


class ReturnType(Statement):
    type = 'return-type'

    _fields = (
        'idl_type',
        'nullable',
        'union',
        'ext_attrs',
        'generic',
    )

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


class Argument(Statement):
    type = 'argument'

    _fields = (
        'name',
        'ext_attrs',
        'idl_type',
        'default',
        'optional',
        'variadic',
    )

    def __init__(self, name, idl_type, ext_attrs=None, default=None, optional=False, variadic=False):
        self.name = name
        self.ext_attrs = ext_attrs or []
        self.idl_type = idl_type
        self.default = default
        self.optional = optional
        self.variadic = variadic

    def accept(self, visitor):
        return visitor.visit_argument(self)


class ArgumentType(Statement):
    type = 'argument-type'

    _fields = (
        'idl_type',
        'nullable',
        'union',
        'ext_attrs',
        'generic',
    )

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
