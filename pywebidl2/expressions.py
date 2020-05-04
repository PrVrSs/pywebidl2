class Expression:
    type: str


class Identifier(Expression):
    type = 'identifier'

    _fields = (
        'value',
    )

    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_identifier(self)


class IdentifierList(Expression):
    type = 'identifier-list'

    _fields = (
        'value',
    )

    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_identifier_list(self)
