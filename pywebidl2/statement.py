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
            inheritance,
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
