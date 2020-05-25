from more_itertools.more import first

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
    Identifier,
    IdentifierList,
    Includes,
    IdlType,
    Infinity,
    Interface,
    InterfaceMixin,
    Iterable_,
    Literal,
    MapLike,
    Namespace,
    Operation,
    Typedef,
    Value,
)
from .generated import WebIDLParser, WebIDLParserVisitor
from .utils import setup_type


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
        setup_type(
            idl_type := ctx.typeWithExtendedAttributes().accept(self),
            'typedef-type',
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
                Identifier(
                    type='enum-value', value=enum_value.getText().strip('"'))
                for enum_value in ctx.STRING_WEBIDL()
            ]
        )

    def visitPartial(self, ctx: WebIDLParser.PartialContext):
        interface_or_mixin = ctx.partialInterfaceOrPartialMixin().accept(self)

        interface_or_mixin.partial = True

        return interface_or_mixin

    def visitInterfaceRest(self, ctx: WebIDLParser.InterfaceRestContext):
        return Interface(
            name=ctx.IDENTIFIER_WEBIDL().getText(),
            inheritance=ctx.inheritance() and ctx.inheritance().accept(self),
            members=[member.accept(self) for member in ctx.interfaceMembers()],
        )

    def visitPartialInterfaceRest(
            self, ctx: WebIDLParser.PartialInterfaceRestContext):
        return Interface(
            name=ctx.IDENTIFIER_WEBIDL().getText(),
            members=[
                member.accept(self) for member in ctx.partialInterfaceMembers()
            ],
        )

    def visitMixinRest(self, ctx: WebIDLParser.MixinRestContext):
        return InterfaceMixin(
            name=ctx.IDENTIFIER_WEBIDL().getText(),
            members=[
                member.accept(self) for member in ctx.mixinMembers()
            ],
        )

    def visitNamespace(self, ctx: WebIDLParser.NamespaceContext):
        return Namespace(
            name=ctx.IDENTIFIER_WEBIDL().getText(),
            members=[
                member.accept(self) for member in ctx.namespaceMembers()
            ],
            partial=ctx.PARTIAL() is not None,
        )

    def visitNamespaceMembers(self, ctx: WebIDLParser.NamespaceMembersContext):
        member = ctx.namespaceMember().accept(self)

        if extended_attribute := ctx.extendedAttributeList():
            member.ext_attrs = extended_attribute.accept(self)

        return member

    def visitMixinMembers(self, ctx: WebIDLParser.MixinMembersContext):
        member = ctx.mixinMember().accept(self)

        if extended_attribute := ctx.extendedAttributeList():
            member.ext_attrs = extended_attribute.accept(self)

        return member

    def visitPartialInterfaceMembers(
            self, ctx: WebIDLParser.PartialInterfaceMembersContext):
        member = ctx.partialInterfaceMember().accept(self)

        if extended_attribute := ctx.extendedAttributeList():
            member.ext_attrs = extended_attribute.accept(self)

        return member

    def visitInterfaceMembers(self, ctx: WebIDLParser.InterfaceMembersContext):
        member = ctx.interfaceMember().accept(self)

        if extended_attribute := ctx.extendedAttributeList():
            member.ext_attrs = extended_attribute.accept(self)

        return member

    def visitDictionaryMembers(
            self, ctx: WebIDLParser.DictionaryMembersContext):
        member = ctx.dictionaryMember().accept(self)

        if extended_attribute := ctx.extendedAttributeList():
            member.ext_attrs = extended_attribute.accept(self)

        return member

    def visitCallbackInterfaceMembers(
            self, ctx: WebIDLParser.CallbackInterfaceMembersContext):
        member = ctx.callbackInterfaceMember().accept(self)

        if extended_attribute := ctx.extendedAttributeList():
            member.ext_attrs = extended_attribute.accept(self)

        return member

    def visitMixinMember(self, ctx: WebIDLParser.MixinMemberContext):
        if ctx.READONLY() is None:
            return ctx.getChild(0).accept(self)

        attribute = ctx.attributeRest().accept(self)
        attribute.readonly = True

        return attribute

    def visitDictionaryMember(self, ctx: WebIDLParser.DictionaryMemberContext):
        if type_ := ctx.typeWithExtendedAttributes():
            idl_type = type_.accept(self)
        else:
            idl_type = ctx.type_().accept(self)

        if default := ctx.default_():
            default = default.accept(self)

        setup_type(idl_type, 'dictionary-type')

        return Field(
            required=ctx.REQUIRED() is not None,
            name=ctx.IDENTIFIER_WEBIDL().getText(),
            default=default,
            idl_type=idl_type,
        )

    def visitNamespaceMember(self, ctx: WebIDLParser.NamespaceMemberContext):
        if regular_operation := ctx.regularOperation():
            return self._operation(regular_operation)

        attribute = ctx.attributeRest().accept(self)
        attribute.readonly = True

        return attribute

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

    def _operation(self, regular_operation, special=''):
        return_type, (name, arguments) = regular_operation.accept(self)

        setup_type(return_type, 'return-type')

        return Operation(
            name=name,
            arguments=arguments,
            idl_type=return_type,
            special=special,
        )

    def visitMaplikeRest(self, ctx: WebIDLParser.MaplikeRestContext):
        return MapLike(
            idl_type=[
                type_with_extended_attr.accept(self)
                for type_with_extended_attr in ctx.typeWithExtendedAttributes()
            ],
            readonly=ctx.READONLY() is not None,
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

        return Identifier(type='number', value=ctx.INTEGER_WEBIDL().getText())

    def visitFloatLiteral(self, ctx: WebIDLParser.FloatLiteralContext):
        if ctx.NAN():
            return Literal(type='NaN')

        if ctx.INFINITY():
            return Infinity(negative=False)

        if ctx.MINUS_INFINITY():
            return Infinity(negative=True)

        return Identifier(type='number', value=ctx.DECIMAL_WEBIDL().getText())

    def visitBooleanLiteral(self, ctx: WebIDLParser.BooleanLiteralContext):
        return Identifier(type='boolean', value=ctx.getText() == 'true')

    def visitConst_(self, ctx: WebIDLParser.Const_Context):
        return Const(
            idl_type=ctx.constType().accept(self),
            value=ctx.constValue().accept(self),
            name=ctx.IDENTIFIER_WEBIDL().getText(),
        )

    def visitCallbackRest(self, ctx: WebIDLParser.CallbackRestContext):
        if arguments := ctx.argumentList():
            arguments = arguments.accept(self)

        setup_type(idl_type := ctx.returnType().accept(self), 'return-type')

        return Callback(
            name=ctx.IDENTIFIER_WEBIDL().getText(),
            idl_type=idl_type,
            arguments=arguments or [],
            ext_attrs=[]
        )

    def visitConstructor(self, ctx: WebIDLParser.ConstructorContext):
        if arguments := ctx.argumentList():
            arguments = arguments.accept(self)

        return Constructor(arguments=arguments or [])

    def visitAttributeRest(self, ctx: WebIDLParser.AttributeRestContext):
        setup_type(
            idl_type := ctx.typeWithExtendedAttributes().accept(self),
            'attribute-type',
        )

        return Attribute(
            name=ctx.attributeName().accept(self), idl_type=idl_type)

    def visitIterable(self, ctx: WebIDLParser.IterableContext):
        if arg_list := ctx.optionalArgumentList():
            arg_list = arg_list.accept(self)

        return Iterable_(
            arguments=arg_list or [],
            async_=ctx.ASYNC() is not None,
            idl_type=[
                type_with_extended_attr.accept(self)
                for type_with_extended_attr in ctx.typeWithExtendedAttributes()
            ],
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
        argument = ctx.argumentRest().accept(self)

        if ext_attrs := ctx.extendedAttributeList():
            argument.ext_attrs = ext_attrs.accept(self)

        return argument

    def visitExtendedAttributeList(
            self, ctx: WebIDLParser.ExtendedAttributeListContext):
        return [
            extendedAttribute.accept(self)
            for extendedAttribute in ctx.extendedAttribute()
        ]

    @staticmethod
    def _extended_attribute(name, rhs=None, arguments=None):
        return ExtendedAttribute(name=name, rhs=rhs, arguments=arguments or [])

    def visitExtendedAttributeNoArgs(
            self, ctx: WebIDLParser.ExtendedAttributeNoArgsContext):
        return self._extended_attribute(ctx.IDENTIFIER_WEBIDL().getText())

    def visitExtendedAttributeNamedArgList(
            self, ctx: WebIDLParser.ExtendedAttributeNamedArgListContext):
        return self._extended_attribute(
            name=ctx.name.text,
            arguments=ctx.argumentList().accept(self),
            rhs=Identifier(type='identifier', value=ctx.rhs.text),
        )

    def visitExtendedAttributeArgList(
            self, ctx: WebIDLParser.ExtendedAttributeArgListContext):
        return self._extended_attribute(
            name=ctx.name.text, arguments=ctx.argumentList().accept(self))

    def visitExtendedAttributeIdentList(
            self, ctx: WebIDLParser.ExtendedAttributeIdentListContext):
        return self._extended_attribute(
            name=ctx.name.text, rhs=ctx.identifierList().accept(self))

    def visitExtendedAttributeIdent(
            self, ctx: WebIDLParser.ExtendedAttributeIdentContext):
        return self._extended_attribute(
            name=ctx.name.text, rhs=ctx.rhs.accept(self))

    def visitIdentifierList(self, ctx: WebIDLParser.IdentifierListContext):
        identifiers = [
            identifier.accept(self) for identifier in ctx.identifier()
        ]

        return IdentifierList(
            value=[Value(value=identifier.value) for identifier in identifiers],
            type=f'{first(identifiers).type}-list',
        )

    def visitArgumentRest(self, ctx: WebIDLParser.ArgumentRestContext):
        if default := ctx.default_():
            default = default.accept(self)

        if optional := ctx.OPTIONAL():
            idl_type = ctx.typeWithExtendedAttributes().accept(self)
        else:
            idl_type = ctx.type_().accept(self)

        setup_type(idl_type, 'argument-type')

        return Argument(
            idl_type=idl_type,
            name=ctx.argumentName().accept(self),
            optional=optional is not None,
            default=default,
        )

    def visitReadOnlyMember(self, ctx: WebIDLParser.ReadOnlyMemberContext):
        member = ctx.readOnlyMemberRest().accept(self)
        member.readonly = True

        return member

    def visitInheritAttribute(self, ctx: WebIDLParser.InheritAttributeContext):
        attribute = ctx.attributeRest().accept(self)
        attribute.special = 'inherit'

        return attribute

    def visitTypeWithExtendedAttributes(
            self, ctx: WebIDLParser.TypeWithExtendedAttributesContext):
        idl_type = ctx.type_().accept(self)

        if ext_attrs := ctx.extendedAttributeList():
            idl_type.ext_attrs = ext_attrs.accept(self)

        return idl_type

    def visitDefault_(self, ctx: WebIDLParser.Default_Context):
        return ctx.defaultValue().accept(self)

    def visitDefaultValue(self, ctx: WebIDLParser.DefaultValueContext):
        if _str := ctx.STRING_WEBIDL():
            return Identifier(type='string', value=_str.getText().strip('"'))

        if const_value := ctx.constValue():
            return const_value.accept(self)

        if ctx.LEFT_BRACE():
            return Literal(type='dictionary')

        if ctx.NULL():
            return Literal(type='null')

        return Identifier(type='sequence', value=[])

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
        nullable = ctx.null_() is not None

        if ext_attrs := ctx.extendedAttributeList():
            ext_attrs = ext_attrs.accept(self)

        if distinguishable_type := ctx.distinguishableType():
            return IdlType(
                idl_type=distinguishable_type.accept(self),
                ext_attrs=ext_attrs or [],
                nullable=nullable,
            )

        if generic := ctx.genericType():
            return IdlType(
                idl_type=[generic.accept(self)],
                ext_attrs=ext_attrs or [],
                nullable=nullable
            )

        return IdlType(
            idl_type=ctx.unionType().accept(self), nullable=nullable)

    def visitReturnType(self, ctx: WebIDLParser.ReturnTypeContext):
        if void := ctx.VOID():
            return IdlType(idl_type=void.getText())

        return ctx.type_().accept(self)

    def visitUnsignedIntegerType(
            self, ctx: WebIDLParser.UnsignedIntegerTypeContext):
        integer_type = ctx.integerType().accept(self)

        if ctx.UNSIGNED():
            integer_type = f'unsigned {integer_type}'

        return integer_type

    def visitSingleType(self, ctx: WebIDLParser.SingleTypeContext):
        nullable = ctx.null_() is not None

        if any_ := ctx.ANY():
            return IdlType(idl_type=any_.getText())

        if promise := ctx.promiseType():
            return IdlType(idl_type=[promise.accept(self)], generic='Promise')

        if generic := ctx.genericType():
            return IdlType(
                idl_type=[generic.accept(self)],
                generic='sequence',
                nullable=nullable,
            )

        return IdlType(
            idl_type=ctx.distinguishableType().accept(self), nullable=nullable)

    def visitGenericType(self, ctx: WebIDLParser.GenericTypeContext):
        return ctx.typeWithExtendedAttributes().accept(self)

    def visitDistinguishableType(
            self, ctx: WebIDLParser.DistinguishableTypeContext):
        if type_ := ctx.primitiveType():
            return type_.accept(self)

        if type_ := ctx.stringType():
            return type_.accept(self)

        if type_ := ctx.bufferRelatedType():
            return type_.accept(self)

        return ctx.getChild(0).getText()

    def visitConstType(self, ctx: WebIDLParser.ConstTypeContext):
        if idl_type := ctx.primitiveType():
            idl_type = idl_type.accept(self)

        return IdlType(
            type='const-type',
            idl_type=idl_type or ctx.IDENTIFIER_WEBIDL().getText(),
        )

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

    def visitPromiseType(self, ctx: WebIDLParser.PromiseTypeContext):
        return ctx.returnType().accept(self)

    def visitIntegerType(self, ctx: WebIDLParser.IntegerTypeContext):
        return ctx.getText()

    def visitFloatType(self, ctx: WebIDLParser.FloatTypeContext):
        return ctx.getText()

    def visitStringType(self, ctx: WebIDLParser.StringTypeContext):
        return ctx.getText()

    def visitOperationName(self, ctx: WebIDLParser.OperationNameContext):
        return ctx.getText()

    def visitArgumentName(self, ctx: WebIDLParser.ArgumentNameContext):
        return ctx.getText()

    def visitAttributeName(self, ctx: WebIDLParser.AttributeNameContext):
        return ctx.getText()

    def visitInheritance(self, ctx: WebIDLParser.InheritanceContext):
        return ctx.IDENTIFIER_WEBIDL().getText()

    def visitOther(self, ctx: WebIDLParser.OtherContext):
        if ctx.INTEGER_WEBIDL():
            type_ = 'integer'
        elif ctx.DECIMAL_WEBIDL():
            type_ = 'decimal'
        elif ctx.STRING_WEBIDL():
            type_ = 'string'
        else:
            type_ = 'identifier'

        return Identifier(type=type_, value=ctx.getText())
