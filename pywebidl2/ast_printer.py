from .visitor import Visitor


class JSONPrinter(Visitor):

    def visit_interface_stmt(self, node):
        return dict(
            type=node.type,
            name=node.name.lexeme,
            extAttrs=[ext_attr.accept(self) for ext_attr in node.ext_attrs],
            members=[member.accept(self) for member in node.members],
            inheritance=node.inheritance,
            partial=node.partial,
        )

    def visit_operation(self, node):
        return dict(
            type=node.type,
            name=node.name.lexeme,
            idlType=node.idl_type.accept(self),
            arguments=[argument.accept(self) for argument in node.arguments],
            special=node.special,
            extAttrs=[ext_attr.accept(self) for ext_attr in node.ext_attrs],
        )

    def visit_argument(self, node):
        return dict(
            name=node.name.lexeme,
            type=node.type,
            idlType=node.idl_type.accept(self),
            default=node.default,
            optional=node.optional,
            variadic=node.variadic,
            extAttrs=[ext_attr.accept(self) for ext_attr in node.ext_attrs],
        )

    def visit_argument_type(self, node):
        return dict(
            type=node.type,
            idlType=node.idl_type.lexeme,
            nullable=node.nullable,
            union=node.union,
            extAttrs=[ext_attr.accept(self) for ext_attr in node.ext_attrs],
            generic=node.generic,
        )

    def visit_return_type(self, node):
        return dict(
            type=node.type,
            idlType=node.idl_type.lexeme,
            nullable=node.nullable,
            union=node.union,
            extAttrs=[ext_attr.accept(self) for ext_attr in node.ext_attrs],
            generic=node.generic,
        )

    def visit_ext_attr(self, node):
        return dict(
            type=node.type,
            name=node.name.lexeme,
            rhs=node.rhs and node.rhs.accept(self) or None,
            arguments=[argument.accept(self) for argument in node.arguments],
        )

    def visit_identifier(self, node):
        return dict(
            type=node.type,
            value=node.value.lexeme,
        )

    def visit_identifier_list(self, node):
        return dict(
            type=node.type,
            value=[{'value': value} for value in node.value],
        )
