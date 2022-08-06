from .idl import parse, parse_as_dict, validate
from .parser import Parser as WebIDLParser
from .visitor import Visitor as WebIDLVisitor

__all__ = (
    'WebIDLParser',
    'WebIDLVisitor',
    'parse',
    'parse_as_dict',
    'validate',
)
