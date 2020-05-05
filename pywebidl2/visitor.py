class Visitor:
    def visit_interface_stmt(self, stmt):
        pass

    def visit_ext_attr(self, stmt):
        pass

    def visit_identifier(self, expr):
        pass

    def visit_identifier_list(self, expr):
        pass

    def visit_operation(self, stmt):
        pass

    def visit_return_type(self, stmt):
        pass

    def visit_argument(self, stmt):
        pass

    def visit_argument_type(self, stmt):
        pass
