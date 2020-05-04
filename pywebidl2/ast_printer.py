from .visitor import Visitor


class JSONPrinter(Visitor):

    def print(self, expr):
        return expr.accept(self)

    def visit_interface_stmt(self, stmt):
        return dict(
            type=stmt.type,
            name=stmt.name,
            extAttrs=[ext_attr.accept(self) for ext_attr in stmt.ext_attrs],
        )

    def visit_ext_attr(self, stmt):
        return dict(
            type=stmt.type,
            name=stmt.name,
            rhs=stmt.rhs.accept(self),
        )

    def visit_identifier(self, expr):
        return dict(
            type=expr.type,
            value=expr.name,
        )

    def visit_identifier_list(self, expr):
        return dict(
            type=expr.type,
            value=[{'value': value} for value in expr.value],
        )
