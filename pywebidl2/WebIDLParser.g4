parser grammar WebIDLParser;

options { tokenVocab=WebIDLLexer; }


webIDL
    : definitions? EOF
;

definitions
    : definition+
;

definition
    : extendedAttributeList? callbackOrInterfaceOrMixin
    | extendedAttributeList? namespace
    | extendedAttributeList? partial
    | extendedAttributeList? dictionary
    | extendedAttributeList? enum_
    | extendedAttributeList? typedef
    | extendedAttributeList? includesStatement
;

callbackOrInterfaceOrMixin
    : CALLBACK callbackRestOrInterface
    | INTERFACE interfaceOrMixin
;

interfaceOrMixin
    : interfaceRest
    | mixinRest
    ;

interfaceRest
    : IDENTIFIER_WEBIDL inheritance? LEFT_BRACE interfaceMembers RIGHT_BRACE SEMI
    ;

partial
    : PARTIAL partialDefinition
;

partialDefinition
    : INTERFACE partialInterfaceOrPartialMixin
    | partialDictionary
    | namespace
    ;

partialInterfaceOrPartialMixin
    : partialInterfaceRest
    | mixinRest
    ;

partialInterfaceRest
    : IDENTIFIER_WEBIDL LEFT_BRACE partialInterfaceMembers RIGHT_BRACE SEMI
    ;

interfaceMembers
    : (extendedAttributeList? interfaceMember)*
    ;

interfaceMember
    : partialInterfaceMember
    | constructor
    ;

partialInterfaceMembers
    : (extendedAttributeList? partialInterfaceMember)*
    ;

partialInterfaceMember
    : const_
    | operation
    | stringifier
    | staticMember
    | iterable
    | asyncIterable
    | readWriteAttribute
    | readWriteMaplike
    | readWriteSetlike
    | inheritAttribute
    ;

inheritance
    : COLON IDENTIFIER_WEBIDL
    ;

mixinRest
    : MIXIN IDENTIFIER_WEBIDL LEFT_BRACE mixinMembers RIGHT_BRACE SEMI
    ;

mixinMembers
    : (extendedAttributeList? mixinMember)*
    ;

mixinMember
    : const_
    | regularOperation
    | stringifier
    | READONLY? attributeRest
    ;

includesStatement
    : IDENTIFIER_WEBIDL INCLUDES IDENTIFIER_WEBIDL SEMI
    ;

callbackRestOrInterface
    : callbackRest
    | INTERFACE IDENTIFIER_WEBIDL LEFT_BRACE callbackInterfaceMembers RIGHT_BRACE SEMI
    ;


callbackInterfaceMembers
    : (extendedAttributeList? callbackInterfaceMember)*
    ;

callbackInterfaceMember
    : const_
    | regularOperation
    ;

const_
    : CONST constType IDENTIFIER_WEBIDL EQUAL_SYMBOL constValue SEMI
    ;

constValue
    : booleanLiteral
    | floatLiteral
    | INTEGER_WEBIDL
    ;

booleanLiteral
    : TRUE
    | FALSE
    ;

floatLiteral
    : DECIMAL_WEBIDL
    | MINUS_INFINITY
    | INFINITY
    | NAN
    ;

constType
    : primitiveType
    | IDENTIFIER_WEBIDL
    ;

readWriteAttribute
    : attributeRest
    ;

inheritAttribute
    : INHERIT attributeRest
    ;

attributeRest
    : READONLY? ATTRIBUTE typeWithExtendedAttributes attributeName SEMI
    ;

attributeName
    : attributeNameKeyword=(ASYNC | REQUIRED)
    | IDENTIFIER_WEBIDL
    ;

defaultValue
    : constValue
    | STRING_WEBIDL
    | LEFT_BRACKET RIGHT_BRACKET
    | LEFT_BRACE RIGHT_BRACE
    | null_
    ;

operation
    : regularOperation
    | specialOperation
    ;

regularOperation
    : returnType operationRest
    ;

specialOperation
    : special=(GETTER | SETTER | DELETER) regularOperation
    ;

operationRest
    : operationName? LEFT_PAREN argumentList? RIGHT_PAREN SEMI
    ;

operationName
    : operationNameKeyword
    | IDENTIFIER_WEBIDL
    ;

operationNameKeyword
    : INCLUDES
    ;

argumentList
    : argument (COMMA argument)*
    ;

argument
    : extendedAttributeList? argumentRest
    ;

argumentRest
    : OPTIONAL typeWithExtendedAttributes argumentName default_?
    | type_ ELLIPSIS? argumentName
    ;

argumentName
    : argumentNameKeyword
    | IDENTIFIER_WEBIDL
    ;

returnType
    : type_
    | VOID
    ;

constructor
    : CONSTRUCTOR LEFT_PAREN argumentList? RIGHT_PAREN SEMI
    ;

stringifier
    : STRINGIFIER stringifierRest
    ;

stringifierRest
    : READONLY? attributeRest
    | regularOperation
    ;

staticMember
    : STATIC staticMemberRest
    ;

staticMemberRest
    : READONLY? attributeRest
    | regularOperation
    ;

iterable
    : ITERABLE LEFT_ANGLE typeWithExtendedAttributes (COMMA typeWithExtendedAttributes)? RIGHT_ANGLE SEMI
    ;

asyncIterable
    : ASYNC ITERABLE LEFT_ANGLE typeWithExtendedAttributes (COMMA typeWithExtendedAttributes)? RIGHT_ANGLE optionalArgumentList? SEMI
    ;

optionalArgumentList
    : LEFT_PAREN argumentList? RIGHT_PAREN
    ;

readWriteMaplike
    : maplikeRest
    ;

maplikeRest
    : READONLY? MAPLIKE LEFT_ANGLE typeWithExtendedAttributes COMMA typeWithExtendedAttributes RIGHT_ANGLE SEMI
    ;

readWriteSetlike
    : setlikeRest
    ;

setlikeRest
    : READONLY? SETLIKE LEFT_ANGLE typeWithExtendedAttributes RIGHT_ANGLE SEMI
    ;

namespace
    : NAMESPACE IDENTIFIER_WEBIDL LEFT_BRACE namespaceMembers RIGHT_BRACE SEMI
    ;

namespaceMembers
    : (extendedAttributeList? namespaceMember)*
    ;

namespaceMember
    : regularOperation
    | READONLY attributeRest
    ;

dictionary
    : DICTIONARY IDENTIFIER_WEBIDL inheritance? LEFT_BRACE dictionaryMembers RIGHT_BRACE SEMI
;

dictionaryMembers
    : (extendedAttributeList? dictionaryMember)*
    ;

dictionaryMember
    : REQUIRED typeWithExtendedAttributes IDENTIFIER_WEBIDL SEMI
    | type_ IDENTIFIER_WEBIDL default_? SEMI
    ;

partialDictionary
    : dictionary IDENTIFIER_WEBIDL LEFT_BRACE dictionaryMembers RIGHT_BRACE SEMI
    ;

default_
    : EQUAL_SYMBOL defaultValue
    ;

enum_
    : ENUM IDENTIFIER_WEBIDL LEFT_BRACE enumValueList RIGHT_BRACE SEMI
    ;

enumValueList
    : STRING_WEBIDL enumValueListComma?
    ;

enumValueListComma
    : COMMA enumValueListString?
    ;

enumValueListString
    : STRING_WEBIDL enumValueListComma?
    ;

callbackRest
    : IDENTIFIER_WEBIDL EQUAL_SYMBOL returnType LEFT_PAREN argumentList? RIGHT_PAREN SEMI
    ;

typedef
    : TYPEDEF typeWithExtendedAttributes IDENTIFIER_WEBIDL SEMI
    ;

type_
    : singleType
    | unionType null_?
    ;

typeWithExtendedAttributes
    : extendedAttributeList? type_
    ;

singleType
    : distinguishableType
    | ANY
    | promiseType
    ;

unionType
    : LEFT_PAREN unionMemberType (OR unionMemberType)+ RIGHT_PAREN
    ;

unionMemberType
    : extendedAttributeList? distinguishableType
    | unionType null_?
    ;

distinguishableType
    : primitiveType null_?
    | stringType null_?
    | IDENTIFIER_WEBIDL null_?
    | SEQUENCE LEFT_ANGLE typeWithExtendedAttributes RIGHT_ANGLE null_?
    | OBJECT null_?
    | SYMBOL null_?
    | bufferRelatedType null_?
    | FROZEN_ARRAY LEFT_ANGLE typeWithExtendedAttributes RIGHT_ANGLE null_?
    | OBSERVABLE_ARRAY LEFT_ANGLE typeWithExtendedAttributes RIGHT_ANGLE null_?
    | recordType null_?
    ;

primitiveType
    : unsignedIntegerType
    | unrestrictedFloatType
    | BOOLEAN
    | BYTE
    | OCTET
    ;

unrestrictedFloatType
    : UNRESTRICTED? floatType
    ;

floatType
    : FLOAT
    | DOUBLE
    ;

unsignedIntegerType
    : UNSIGNED? integerType
    ;

integerType
    : SHORT
    | LONG optionalLong?
    ;

optionalLong
    : LONG
    ;

stringType
    : BYTE_STRING
    | DOM_STRING
    | USV_STRING
    ;

promiseType
    : PROMISE LEFT_ANGLE returnType RIGHT_ANGLE
    ;

recordType
    : RECORD LEFT_ANGLE stringType COMMA typeWithExtendedAttributes RIGHT_ANGLE
    ;

null_
    : QUESTION_SYMBOL
    ;

bufferRelatedType
    : ARRAY_BUFFER
    | DATA_VIEW
    | INT_8_ARRAY
    | INT_16_ARRAY
    | INT_32_ARRAY
    | UINT_8_ARRAY
    | UINT_16_ARRAY
    | UINT_32_ARRAY
    | UINT_8_CLAMPED_ARRAY
    | FLOAT_32_ARRAY
    | FLOAT_64_ARRAY
    ;

extendedAttributeList
    : LEFT_BRACKET extendedAttribute (COMMA extendedAttribute)* RIGHT_BRACKET
    ;

extendedAttribute
    : LEFT_PAREN extendedAttributeInner? RIGHT_PAREN extendedAttribute?
    | LEFT_BRACKET extendedAttributeInner? RIGHT_BRACKET extendedAttribute?
    | LEFT_BRACE extendedAttributeInner? RIGHT_BRACE extendedAttribute?
    | other extendedAttribute?
    ;

extendedAttributeInner
    : LEFT_PAREN extendedAttributeInner? RIGHT_PAREN extendedAttributeInner?
    | LEFT_BRACKET extendedAttributeInner? RIGHT_BRACKET extendedAttributeInner?
    | LEFT_BRACE extendedAttributeInner? RIGHT_BRACE extendedAttributeInner?
    | otherOrComma extendedAttributeInner?
    ;

other
    : INTEGER_WEBIDL
    | DECIMAL_WEBIDL
    | IDENTIFIER_WEBIDL
    | STRING_WEBIDL
    | OTHER_WEBIDL
    | MINUS
    | MINUS_INFINITY
    | DOT
    | ELLIPSIS
    | COLON
    | SEMI
    | LEFT_ANGLE
    | EQUAL_SYMBOL
    | RIGHT_ANGLE
    | QUESTION_SYMBOL
    | BYTE_STRING
    | DOM_STRING
    | FROZEN_ARRAY
    | INFINITY
    | NAN
    | OBSERVABLE_ARRAY
    | PROMISE
    | USV_STRING
    | ANY
    | BOOLEAN
    | BYTE
    | DOUBLE
    | FALSE
    | FLOAT
    | LONG
    | NULL
    | OBJECT
    | OCTET
    | OR
    | OPTIONAL
    | RECORD
    | SEQUENCE
    | SHORT
    | SYMBOL
    | TRUE
    | UNSIGNED
    | VOID
    | argumentNameKeyword
    | bufferRelatedType
    ;

otherOrComma
    : other
    | COMMA
    ;

argumentNameKeyword
    : ASYNC
    | ATTRIBUTE
    | CALLBACK
    | CONST
    | CONSTRUCTOR
    | DELETER
    | DICTIONARY
    | ENUM
    | GETTER
    | INCLUDES
    | INHERIT
    | INTERFACE
    | ITERABLE
    | MAPLIKE
    | MIXIN
    | NAMESPACE
    | PARTIAL
    | READONLY
    | REQUIRED
    | SETLIKE
    | SETTER
    | STATIC
    | STRINGIFIER
    | TYPEDEF
    | UNRESTRICTED
    ;
