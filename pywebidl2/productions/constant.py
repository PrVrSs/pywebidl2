TYPE_NAME_KEYWORDS = frozenset((
    'ArrayBuffer',
    'DataView',
    'Int8Array',
    'Int16Array',
    'Int32Array',
    'Uint8Array',
    'Uint16Array',
    'Uint32Array',
    'Uint8ClampedArray',
    'Float32Array',
    'Float64Array',
    'any',
    'object',
    'symbol'
))

STRING_TYPES = frozenset((
    'ByteString',
    'DOMString',
    'USVString',
))

ARGUMENT_NAME_KEYWORDS = frozenset((
    'async',
    'attribute',
    'callback',
    'const',
    'constructor',
    'deleter',
    'dictionary',
    'enum',
    'getter',
    'includes',
    'inherit',
    'interface',
    'iterable',
    'maplike',
    'namespace',
    'partial',
    'required',
    'setlike',
    'setter',
    'static',
    'stringifier',
    'typedef',
    'unrestricted',
))

SPECIAL = frozenset((
    '-Infinity',
    'FrozenArray',
    'Infinity',
    'NaN',
    'Promise',
    'boolean',
    'byte',
    'double',
    'false',
    'float',
    'long',
    'mixin',
    'null',
    'octet',
    'optional',
    'or',
    'readonly',
    'record',
    'sequence',
    'short',
    'true',
    'unsigned',
    'void',
))

PUNCTUATIONS = frozenset((
    '(',
    ')',
    ',',
    '...',
    ':',
    ';',
    '<',
    '=',
    '>',
    '?',
    '[',
    ']',
    '{',
    '}',
))

NON_TERMINALS = frozenset(
    ARGUMENT_NAME_KEYWORDS | STRING_TYPES | TYPE_NAME_KEYWORDS | SPECIAL)
