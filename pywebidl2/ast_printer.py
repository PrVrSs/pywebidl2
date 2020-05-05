from .visitor import Visitor


class JSONPrinter(Visitor):

    def print(self, expr):
        return expr.accept(self)

    def visit_interface_stmt(self, stmt):
        return dict(
            type=stmt.type,
            name=stmt.name.lexeme,
            extAttrs=[ext_attr.accept(self) for ext_attr in stmt.ext_attrs],
            members=[member.accept(self) for member in stmt.members],
            inheritance=stmt.inheritance,
            partial=stmt.partial,
        )

    def visit_operation(self, stmt):
        return dict(
            type=stmt.type,
            name=stmt.name.lexeme,
            idlType=stmt.idl_type.accept(self),
            arguments=[argument.accept(self) for argument in stmt.arguments],
            special=stmt.special,
            extAttrs=[ext_attr.accept(self) for ext_attr in stmt.ext_attrs],
        )

    def visit_argument(self, stmt):
        return dict(
            name=stmt.name.lexeme,
            type=stmt.type,
            idlType=stmt.idl_type.accept(self),
            default=stmt.default,
            optional=stmt.optional,
            variadic=stmt.variadic,
            extAttrs=[ext_attr.accept(self) for ext_attr in stmt.ext_attrs],
        )

    def visit_argument_type(self, stmt):
        return dict(
            type=stmt.type,
            idlType=stmt.idl_type.lexeme,
            nullable=stmt.nullable,
            union=stmt.union,
            extAttrs=[ext_attr.accept(self) for ext_attr in stmt.ext_attrs],
            generic=stmt.generic,
        )

    def visit_return_type(self, stmt):
        return dict(
            type=stmt.type,
            idlType=stmt.idl_type.lexeme,
            nullable=stmt.nullable,
            union=stmt.union,
            extAttrs=[ext_attr.accept(self) for ext_attr in stmt.ext_attrs],
            generic=stmt.generic,
        )

    def visit_ext_attr(self, stmt):
        return dict(
            type=stmt.type,
            name=stmt.name.lexeme,
            rhs=stmt.rhs and stmt.rhs.accept(self) or None,
            arguments=[argument.accept(self) for argument in stmt.arguments],
        )

    def visit_identifier(self, expr):
        return dict(
            type=expr.type,
            value=expr.name.lexeme,
        )

    def visit_identifier_list(self, expr):
        return dict(
            type=expr.type,
            value=[{'value': value} for value in expr.value],
        )
