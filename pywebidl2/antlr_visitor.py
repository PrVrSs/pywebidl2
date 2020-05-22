from .expr import (
    Argument,
    Attribute,
    Callback,
    CallbackInterface,
    Const,
    Constructor,
    Dictionary,
    Enum,
    ExtendedAttribute,
    Field,
    Includes,
    IdlType,
    Infinity,
    Interface,
    Iterable_,
    Literal,
    Operation,
    Typedef,
    Value,
)
from .generated import WebIDLParser, WebIDLParserVisitor


class Visitor(WebIDLParserVisitor):  # pylint: disable=too-many-public-methods

    def __init__(self, tree):
        self._tree = tree

    def run(self):
        return self.visit(self._tree)

    def visitWebIDL(self, ctx: WebIDLParser.WebIDLContext):
        return ctx.definitions().accept(self)

    def visitDefinitions(self, ctx: WebIDLParser.DefinitionsContext):
        return [
            definition.accept(self) for definition in ctx.extendedDefinition()
        ]

    def visitExtendedDefinition(
            self, ctx: WebIDLParser.ExtendedDefinitionContext):
        definition = ctx.definition().accept(self)

        if extended_attribute := ctx.extendedAttributeList():
            definition.ext_attrs = extended_attribute.accept(self)

        return definition

    def visitDictionary(self, ctx: WebIDLParser.DictionaryContext):
        return Dictionary(
            partial=ctx.PARTIAL() is not None,
            name=ctx.IDENTIFIER_WEBIDL().getText(),
            members=[member.accept(self) for member in ctx.dictionaryMembers()],
            inheritance=ctx.inheritance() and ctx.inheritance().accept(self),
        )

    def visitTypedef(self, ctx: WebIDLParser.TypedefContext):
        self._setup_type(
            idl_type := ctx.typeWithExtendedAttributes().accept(self),
            _type='typedef-type',
        )

        return Typedef(
            idl_type=idl_type, name=ctx.IDENTIFIER_WEBIDL().getText())

    def visitIncludesStatement(
            self, ctx: WebIDLParser.IncludesStatementContext):
        return Includes(
            target=ctx.target.text, includes=ctx.includes.text)  # type: ignore

    def visitEnum_(self, ctx: WebIDLParser.Enum_Context):
        return Enum(
            name=ctx.IDENTIFIER_WEBIDL().getText(),
            values=[
                Value(type='enum-value', value=enum_value.getText().strip('"'))
                for enum_value in ctx.STRING_WEBIDL()
            ]
        )

    def visitInheritance(self, ctx: WebIDLParser.InheritanceContext):
        return ctx.IDENTIFIER_WEBIDL().getText()

    def visitDictionaryMembers(
            self, ctx: WebIDLParser.DictionaryMembersContext):
        member = ctx.dictionaryMember().accept(self)

        if extended_attribute := ctx.extendedAttributeList():
            member.ext_attrs = extended_attribute.accept(self)

        return member

    @staticmethod
    def _setup_type(idl_type, _type):
        idl_type.type = _type

        if idl_type.generic == 'sequence':
            for idl in idl_type.idl_type:
                idl.type = _type

    def visitDictionaryMember(self, ctx: WebIDLParser.DictionaryMemberContext):
        if type_ := ctx.typeWithExtendedAttributes():
            idl_type = type_.accept(self)
        else:
            idl_type = ctx.type_().accept(self)

        if default := ctx.default_():
            default = default.accept(self)

        self._setup_type(idl_type, 'dictionary-type')

        return Field(
            required=ctx.REQUIRED() is not None,
            name=ctx.IDENTIFIER_WEBIDL().getText(),
            default=default,
            idl_type=idl_type,
        )

    def visitCallbackOrInterfaceOrMixin(
            self, ctx: WebIDLParser.CallbackOrInterfaceOrMixinContext):
        if callback := ctx.callbackRestOrInterface():
            return callback.accept(self)

        return ctx.interfaceOrMixin().accept(self)

    def visitCallbackRestOrInterface(
            self, ctx: WebIDLParser.CallbackRestOrInterfaceContext):
        if callback_rest := ctx.callbackRest():
            return callback_rest.accept(self)

        return CallbackInterface(
            name=ctx.IDENTIFIER_WEBIDL().getText(),
            inheritance=None,
            members=[
                member.accept(self)
                for member in ctx.callbackInterfaceMembers()
            ],
        )

    def visitInterfaceOrMixin(self, ctx: WebIDLParser.InterfaceOrMixinContext):
        if interface_rest := ctx.interfaceRest():
            return interface_rest.accept(self)

        return ctx.mixinRest().accept(self)

    def visitCallbackInterfaceMembers(
            self, ctx: WebIDLParser.CallbackInterfaceMembersContext):
        member = ctx.callbackInterfaceMember().accept(self)

        if extended_attribute := ctx.extendedAttributeList():
            member.ext_attrs = extended_attribute.accept(self)

        return member

    def _operation(self, regular_operation, special=''):
        return_type, (name, arguments) = regular_operation.accept(self)

        return Operation(
            name=name,
            arguments=arguments,
            idl_type=IdlType(type='return-type', idl_type=return_type),
            special=special,
        )

    def visitCallbackInterfaceMember(
            self, ctx: WebIDLParser.CallbackInterfaceMemberContext):
        if regular_operation := ctx.regularOperation():
            return self._operation(regular_operation)

        return ctx.const_()

    def visitConstValue(self, ctx: WebIDLParser.ConstValueContext):
        if boolean_literal := ctx.booleanLiteral():
            return boolean_literal.accept(self)

        if float_literal := ctx.floatLiteral():
            return float_literal.accept(self)

        return Value(type='number', value=ctx.INTEGER_WEBIDL().getText())

    def visitFloatLiteral(self, ctx: WebIDLParser.FloatLiteralContext):
        if ctx.NAN():
            return Literal(type='NaN')

        if ctx.INFINITY():
            return Infinity(negative=False)

        if ctx.MINUS_INFINITY():
            return Infinity(negative=True)

        return Value(type='number', value=ctx.DECIMAL_WEBIDL().getText())

    def visitBooleanLiteral(self, ctx: WebIDLParser.BooleanLiteralContext):
        return Value(type='boolean', value=ctx.getText() == 'true')

    def visitConst_(self, ctx: WebIDLParser.Const_Context):
        return Const(
            idl_type=ctx.constType().accept(self),
            value=ctx.constValue().accept(self),
            name=ctx.IDENTIFIER_WEBIDL().getText(),
        )

    def visitConstType(self, ctx: WebIDLParser.ConstTypeContext):
        if idl_type := ctx.primitiveType():
            idl_type = idl_type.accept(self)

        return IdlType(
            type='const-type',
            idl_type=idl_type or ctx.IDENTIFIER_WEBIDL().getText(),
        )

    def visitCallbackRest(self, ctx: WebIDLParser.CallbackRestContext):
        if arguments := ctx.argumentList():
            arguments = arguments.accept(self)

        idl_type = IdlType(
            type='return-type',
            idl_type=ctx.returnType().accept(self),
        )

        return Callback(
            name=ctx.IDENTIFIER_WEBIDL().getText(),
            idl_type=idl_type,
            arguments=arguments or [],
            ext_attrs=[]
        )

    def visitInterfaceRest(self, ctx: WebIDLParser.InterfaceRestContext):
        return Interface(
            name=ctx.IDENTIFIER_WEBIDL().getText(),
            inheritance=ctx.inheritance() and ctx.inheritance().accept(self),
            members=[member.accept(self) for member in ctx.interfaceMembers()],
            partial=False,
        )

    def visitInterfaceMembers(self, ctx: WebIDLParser.InterfaceMembersContext):
        member = ctx.interfaceMember().accept(self)

        if extended_attribute := ctx.extendedAttributeList():
            member.ext_attrs = extended_attribute.accept(self)

        return member

    def visitPartialInterfaceMember(
            self, ctx: WebIDLParser.PartialInterfaceMemberContext):
        return ctx.getChild(0).accept(self)

    def visitConstructor(self, ctx: WebIDLParser.ConstructorContext):
        if arguments := ctx.argumentList():
            arguments = arguments.accept(self)

        return Constructor(arguments=arguments or [])

    def visitIntegerType(self, ctx: WebIDLParser.IntegerTypeContext):
        return ctx.getText()

    def visitUnsignedIntegerType(
            self, ctx: WebIDLParser.UnsignedIntegerTypeContext):
        integer_type = ctx.integerType().accept(self)

        if ctx.UNSIGNED():
            integer_type = f'unsigned {integer_type}'

        return integer_type

    def visitSingleType(self, ctx: WebIDLParser.SingleTypeContext):
        if any_ := ctx.ANY():
            return IdlType(idl_type=any_.getText())

        return ctx.getChild(0).accept(self)

    def visitDistinguishableType(
            self, ctx: WebIDLParser.DistinguishableTypeContext):
        null = ctx.null_() is not None

        if type_ := ctx.primitiveType():
            return IdlType(idl_type=type_.accept(self), nullable=null)

        if type_ := ctx.stringType():
            return IdlType(idl_type=type_.accept(self), nullable=null)

        if type_ := ctx.typeWithExtendedAttributes():
            return IdlType(
                idl_type=[type_.accept(self)],
                nullable=null,
                generic=ctx.SEQUENCE() and ctx.SEQUENCE().getText() or '',
            )

        if type_ := ctx.bufferRelatedType():
            return IdlType(idl_type=type_.accept(self), nullable=null)

        return IdlType(idl_type=ctx.getChild(0).getText(), nullable=null)

    def visitPrimitiveType(self, ctx: WebIDLParser.PrimitiveTypeContext):
        if type_ := ctx.unsignedIntegerType():
            return type_.accept(self)

        if type_ := ctx.unrestrictedFloatType():
            return type_.accept(self)

        return ctx.getChild(0).getText()

    def visitUnrestrictedFloatType(
            self, ctx: WebIDLParser.UnrestrictedFloatTypeContext):
        float_type = ctx.floatType().accept(self)

        if ctx.UNRESTRICTED():
            float_type = f'unrestricted {float_type}'

        return float_type

    def visitFloatType(self, ctx: WebIDLParser.FloatTypeContext):
        return ctx.getText()

    def visitAttributeRest(self, ctx: WebIDLParser.AttributeRestContext):
        idl_type = ctx.typeWithExtendedAttributes().accept(self)
        idl_type.type = 'attribute-type'

        return Attribute(
            name=ctx.attributeName().accept(self),
            idl_type=idl_type,
            ext_attrs=[],
            readonly=ctx.READONLY() is not None,
            special=''
        )

    def visitAttributeName(self, ctx: WebIDLParser.AttributeNameContext):
        return ctx.getText()

    def visitReadWriteAttribute(
            self, ctx: WebIDLParser.ReadWriteAttributeContext):
        return ctx.getChild(0).accept(self)

    # def visitIterable(self, ctx: WebIDLParser.IterableContext):
    #     idl_type = ctx.typeWithExtendedAttributes().accept(self)
    #
    #     return Iterable_(
    #         idl_type=idl_type,
    #         arguments=[],
    #         ext_attrs=[],
    #         async_=False,
    #         readonly=False,
    #     )

    def visitAsyncIterable(self, ctx: WebIDLParser.AsyncIterableContext):
        idl_types = []
        for type_with_extended_attr in ctx.typeWithExtendedAttributes():
            idl_types.append(type_with_extended_attr.accept(self))

        if arg_list := ctx.optionalArgumentList():
            arg_list = arg_list.accept(self)

        return Iterable_(
            idl_type=idl_types,
            arguments=arg_list or [],
            ext_attrs=[],
            async_=True,
            readonly=False,
        )

    def visitOptionalArgumentList(
            self, ctx: WebIDLParser.OptionalArgumentListContext):
        if arg_list := ctx.argumentList():
            arg_list = arg_list.accept(self)

        return arg_list or []

    def visitOperation(self, ctx: WebIDLParser.OperationContext):
        return self._operation(
            ctx.regularOperation(), ctx.special and ctx.special.text or '')

    def visitRegularOperation(self, ctx: WebIDLParser.RegularOperationContext):
        return ctx.returnType().accept(self), ctx.operationRest().accept(self)

    def visitOperationRest(self, ctx: WebIDLParser.OperationRestContext):
        if name := ctx.operationName():
            name = name.accept(self)

        if arguments := ctx.argumentList():
            arguments = arguments.accept(self)

        return name or '', arguments or []

    def visitArgumentList(self, ctx: WebIDLParser.ArgumentListContext):
        return [argument.accept(self) for argument in ctx.argument()]

    def visitArgument(self, ctx: WebIDLParser.ArgumentContext):
        if ext_attrs := ctx.extendedAttributeList():
            ext_attrs = ext_attrs.accept(self)

        optional, arg_name, idl_type, default = ctx.argumentRest().accept(self)

        return Argument(
            ext_attrs=ext_attrs or [],
            idl_type=idl_type,
            name=arg_name,
            optional=optional,
            default=default,
        )

    def visitExtendedAttributeList(
            self, ctx: WebIDLParser.ExtendedAttributeListContext):
        return [
            extendedAttribute.accept(self)
            for extendedAttribute in ctx.extendedAttribute()
        ]

    def visitExtendedAttribute(
            self, ctx: WebIDLParser.ExtendedAttributeContext):
        if name := ctx.other():
            name = name.accept(self)

        if name == '=':
            return Value(
                type='identifier', value=ctx.extendedAttribute().getText())

        if rhs := ctx.extendedAttribute():
            rhs = rhs.accept(self)

        return ExtendedAttribute(
            name=name,
            rhs=rhs,
            arguments=[],
        )

    def visitOther(self, ctx: WebIDLParser.OtherContext):
        return ctx.getText()

    def visitOtherOrComma(self, ctx: WebIDLParser.OtherOrCommaContext):
        return ctx.getText()

    def visitArgumentRest(self, ctx: WebIDLParser.ArgumentRestContext):
        if default := ctx.default_():
            default = default.accept(self)

        if ctx.getChild(0).getText() == 'optional':
            optional = True
            idl_type = ctx.typeWithExtendedAttributes().accept(self)
        else:
            optional = False
            idl_type = ctx.type_().accept(self)

        arg_name = ctx.argumentName().accept(self)

        self._setup_type(idl_type, 'argument-type')

        return optional, arg_name, idl_type, default

    def visitStringType(self, ctx: WebIDLParser.StringTypeContext):
        return ctx.getText()

    def visitTypeWithExtendedAttributes(
            self, ctx: WebIDLParser.TypeWithExtendedAttributesContext):
        idl_type = ctx.type_().accept(self)

        if ext_attrs := ctx.extendedAttributeList():
            idl_type.ext_attrs = ext_attrs.accept(self)

        return idl_type

    def visitArgumentName(self, ctx: WebIDLParser.ArgumentNameContext):
        return ctx.getText()

    def visitType_(self, ctx: WebIDLParser.Type_Context):
        if single_type := ctx.singleType():
            return single_type.accept(self)

        return IdlType(
            idl_type=ctx.unionType().accept(self),
            nullable=ctx.null_() is not None,
            union=True,
        )

    def visitUnionType(self, ctx: WebIDLParser.UnionTypeContext):
        return [
            member_type.accept(self) for member_type in ctx.unionMemberType()
        ]

    def visitUnionMemberType(self, ctx: WebIDLParser.UnionMemberTypeContext):
        if ext_attrs := ctx.extendedAttributeList():
            ext_attrs = ext_attrs.accept(self)

        if distinguishable_type := ctx.distinguishableType():
            idl_type = distinguishable_type.accept(self)
            idl_type.ext_attrs = ext_attrs or []
            return idl_type

        return IdlType(
            idl_type=ctx.unionType().accept(self),
            nullable=ctx.null_() is not None,
        )

    def visitDefault_(self, ctx: WebIDLParser.Default_Context):
        return ctx.defaultValue().accept(self)

    def visitDefaultValue(self, ctx: WebIDLParser.DefaultValueContext):
        if _str := ctx.STRING_WEBIDL():
            return Value(type='string', value=_str.getText().strip('"'))

        if const_value := ctx.constValue():
            return const_value.accept(self)

        if ctx.LEFT_BRACE():
            return Literal(type='dictionary')

        if ctx.NULL():
            return Literal(type='null')

        return Value(type='sequence', value=[])

    def visitOperationName(self, ctx: WebIDLParser.OperationNameContext):
        return ctx.getText()

    def visitReturnType(self, ctx: WebIDLParser.ReturnTypeContext):
        return ctx.getText()
