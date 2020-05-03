class Expression:
    type: str


class Identifier(Expression):
    type = 'identifier'

    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_identifier(self)
