# Generated from WebIDLParser.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .WebIDLParser import WebIDLParser
else:
    from WebIDLParser import WebIDLParser

# This class defines a complete generic visitor for a parse tree produced by WebIDLParser.

class WebIDLParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by WebIDLParser#webIDL.
    def visitWebIDL(self, ctx:WebIDLParser.WebIDLContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#definitions.
    def visitDefinitions(self, ctx:WebIDLParser.DefinitionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#extendedDefinition.
    def visitExtendedDefinition(self, ctx:WebIDLParser.ExtendedDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#definition.
    def visitDefinition(self, ctx:WebIDLParser.DefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#callbackOrInterfaceOrMixin.
    def visitCallbackOrInterfaceOrMixin(self, ctx:WebIDLParser.CallbackOrInterfaceOrMixinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#interfaceOrMixin.
    def visitInterfaceOrMixin(self, ctx:WebIDLParser.InterfaceOrMixinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#interfaceRest.
    def visitInterfaceRest(self, ctx:WebIDLParser.InterfaceRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#partial.
    def visitPartial(self, ctx:WebIDLParser.PartialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#partialInterfaceOrPartialMixin.
    def visitPartialInterfaceOrPartialMixin(self, ctx:WebIDLParser.PartialInterfaceOrPartialMixinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#partialInterfaceRest.
    def visitPartialInterfaceRest(self, ctx:WebIDLParser.PartialInterfaceRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#interfaceMembers.
    def visitInterfaceMembers(self, ctx:WebIDLParser.InterfaceMembersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#interfaceMember.
    def visitInterfaceMember(self, ctx:WebIDLParser.InterfaceMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#partialInterfaceMembers.
    def visitPartialInterfaceMembers(self, ctx:WebIDLParser.PartialInterfaceMembersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#partialInterfaceMember.
    def visitPartialInterfaceMember(self, ctx:WebIDLParser.PartialInterfaceMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#inheritance.
    def visitInheritance(self, ctx:WebIDLParser.InheritanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#mixinRest.
    def visitMixinRest(self, ctx:WebIDLParser.MixinRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#mixinMembers.
    def visitMixinMembers(self, ctx:WebIDLParser.MixinMembersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#mixinMember.
    def visitMixinMember(self, ctx:WebIDLParser.MixinMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#includesStatement.
    def visitIncludesStatement(self, ctx:WebIDLParser.IncludesStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#callbackRestOrInterface.
    def visitCallbackRestOrInterface(self, ctx:WebIDLParser.CallbackRestOrInterfaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#callbackInterfaceMembers.
    def visitCallbackInterfaceMembers(self, ctx:WebIDLParser.CallbackInterfaceMembersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#callbackInterfaceMember.
    def visitCallbackInterfaceMember(self, ctx:WebIDLParser.CallbackInterfaceMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#const_.
    def visitConst_(self, ctx:WebIDLParser.Const_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#constValue.
    def visitConstValue(self, ctx:WebIDLParser.ConstValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#booleanLiteral.
    def visitBooleanLiteral(self, ctx:WebIDLParser.BooleanLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#floatLiteral.
    def visitFloatLiteral(self, ctx:WebIDLParser.FloatLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#constType.
    def visitConstType(self, ctx:WebIDLParser.ConstTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#readWriteAttribute.
    def visitReadWriteAttribute(self, ctx:WebIDLParser.ReadWriteAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#inheritAttribute.
    def visitInheritAttribute(self, ctx:WebIDLParser.InheritAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#attributeRest.
    def visitAttributeRest(self, ctx:WebIDLParser.AttributeRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#attributeName.
    def visitAttributeName(self, ctx:WebIDLParser.AttributeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#defaultValue.
    def visitDefaultValue(self, ctx:WebIDLParser.DefaultValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#operation.
    def visitOperation(self, ctx:WebIDLParser.OperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#regularOperation.
    def visitRegularOperation(self, ctx:WebIDLParser.RegularOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#operationRest.
    def visitOperationRest(self, ctx:WebIDLParser.OperationRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#operationName.
    def visitOperationName(self, ctx:WebIDLParser.OperationNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#operationNameKeyword.
    def visitOperationNameKeyword(self, ctx:WebIDLParser.OperationNameKeywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#argumentList.
    def visitArgumentList(self, ctx:WebIDLParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#argument.
    def visitArgument(self, ctx:WebIDLParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#argumentRest.
    def visitArgumentRest(self, ctx:WebIDLParser.ArgumentRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#argumentName.
    def visitArgumentName(self, ctx:WebIDLParser.ArgumentNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#returnType.
    def visitReturnType(self, ctx:WebIDLParser.ReturnTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#constructor.
    def visitConstructor(self, ctx:WebIDLParser.ConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#stringifier.
    def visitStringifier(self, ctx:WebIDLParser.StringifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#stringifierRest.
    def visitStringifierRest(self, ctx:WebIDLParser.StringifierRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#staticMember.
    def visitStaticMember(self, ctx:WebIDLParser.StaticMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#staticMemberRest.
    def visitStaticMemberRest(self, ctx:WebIDLParser.StaticMemberRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#iterable.
    def visitIterable(self, ctx:WebIDLParser.IterableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#optionalArgumentList.
    def visitOptionalArgumentList(self, ctx:WebIDLParser.OptionalArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#readWriteMaplike.
    def visitReadWriteMaplike(self, ctx:WebIDLParser.ReadWriteMaplikeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#maplikeRest.
    def visitMaplikeRest(self, ctx:WebIDLParser.MaplikeRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#readWriteSetlike.
    def visitReadWriteSetlike(self, ctx:WebIDLParser.ReadWriteSetlikeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#setlikeRest.
    def visitSetlikeRest(self, ctx:WebIDLParser.SetlikeRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#namespace.
    def visitNamespace(self, ctx:WebIDLParser.NamespaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#namespaceMembers.
    def visitNamespaceMembers(self, ctx:WebIDLParser.NamespaceMembersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#namespaceMember.
    def visitNamespaceMember(self, ctx:WebIDLParser.NamespaceMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#dictionary.
    def visitDictionary(self, ctx:WebIDLParser.DictionaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#dictionaryMembers.
    def visitDictionaryMembers(self, ctx:WebIDLParser.DictionaryMembersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#dictionaryMember.
    def visitDictionaryMember(self, ctx:WebIDLParser.DictionaryMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#default_.
    def visitDefault_(self, ctx:WebIDLParser.Default_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#enum_.
    def visitEnum_(self, ctx:WebIDLParser.Enum_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#callbackRest.
    def visitCallbackRest(self, ctx:WebIDLParser.CallbackRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#typedef.
    def visitTypedef(self, ctx:WebIDLParser.TypedefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#type_.
    def visitType_(self, ctx:WebIDLParser.Type_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#typeWithExtendedAttributes.
    def visitTypeWithExtendedAttributes(self, ctx:WebIDLParser.TypeWithExtendedAttributesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#singleType.
    def visitSingleType(self, ctx:WebIDLParser.SingleTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#unionType.
    def visitUnionType(self, ctx:WebIDLParser.UnionTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#unionMemberType.
    def visitUnionMemberType(self, ctx:WebIDLParser.UnionMemberTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#genericType.
    def visitGenericType(self, ctx:WebIDLParser.GenericTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#distinguishableType.
    def visitDistinguishableType(self, ctx:WebIDLParser.DistinguishableTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#primitiveType.
    def visitPrimitiveType(self, ctx:WebIDLParser.PrimitiveTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#unrestrictedFloatType.
    def visitUnrestrictedFloatType(self, ctx:WebIDLParser.UnrestrictedFloatTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#floatType.
    def visitFloatType(self, ctx:WebIDLParser.FloatTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#unsignedIntegerType.
    def visitUnsignedIntegerType(self, ctx:WebIDLParser.UnsignedIntegerTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#integerType.
    def visitIntegerType(self, ctx:WebIDLParser.IntegerTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#stringType.
    def visitStringType(self, ctx:WebIDLParser.StringTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#promiseType.
    def visitPromiseType(self, ctx:WebIDLParser.PromiseTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#recordType.
    def visitRecordType(self, ctx:WebIDLParser.RecordTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#null_.
    def visitNull_(self, ctx:WebIDLParser.Null_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#bufferRelatedType.
    def visitBufferRelatedType(self, ctx:WebIDLParser.BufferRelatedTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#extendedAttributeList.
    def visitExtendedAttributeList(self, ctx:WebIDLParser.ExtendedAttributeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#extendedAttribute.
    def visitExtendedAttribute(self, ctx:WebIDLParser.ExtendedAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#extendedAttributeInner.
    def visitExtendedAttributeInner(self, ctx:WebIDLParser.ExtendedAttributeInnerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#other.
    def visitOther(self, ctx:WebIDLParser.OtherContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#otherOrComma.
    def visitOtherOrComma(self, ctx:WebIDLParser.OtherOrCommaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by WebIDLParser#argumentNameKeyword.
    def visitArgumentNameKeyword(self, ctx:WebIDLParser.ArgumentNameKeywordContext):
        return self.visitChildren(ctx)



del WebIDLParser