# pywebidl2
[![Build Status](https://github.com/PrVrSs/pywebidl2/workflows/test/badge.svg?branch=master&event=push)](https://github.com/PrVrSs/pywebidl2/actions?query=workflow%3Atest)
[![Codecov](https://codecov.io/gh/PrVrSs/pywebidl2/branch/master/graph/badge.svg)](https://codecov.io/gh/PrVrSs/pywebidl2)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/PrVrSs/pywebidl2/blob/master/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)

## Description

*This is a tool for the [Web IDL](https://heycam.github.io/webidl/) language.*

## Quick start

```shell script
pip install pywebidl2
```

### Usage

```
Usage: pywebidl2 [OPTIONS] FILE

Options:
  -a, --action [parse|validate]
  --help                         Show this message and exit.
```

## For Developer

### Antlr4

*Download* [ANTLR4 tool](https://www.antlr.org/download/antlr-4.11.1-complete.jar)

[Getting Started with ANTLR v4](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md)

### Create a python parser and lexer.
```shell script
make parser
```

### Tests

```shell script
make test
```

## Example

### Parser

```python
from pprint import pprint

from pywebidl2 import parse


idl = '''
    interface B {
      void g([AllowAny] DOMString s);
    };
'''

pprint(parse(idl))
```

```json
[
    {
        "type": "interface",
        "name": "B",
        "inheritance": null,
        "members": [
            {
                "type": "operation",
                "name": "g",
                "idl_type": {
                    "type": "return-type",
                    "ext_attrs": [],
                    "generic": "",
                    "nullable": false,
                    "union": false,
                    "idl_type": "void"
                },
                "arguments": [
                    {
                        "type": "argument",
                        "name": "s",
                        "ext_attrs": [
                            {
                                "type": "extended-attribute",
                                "name": "AllowAny",
                                "rhs": null,
                                "arguments": []
                            }
                        ],
                        "idl_type": {
                            "type": "argument-type",
                            "ext_attrs": [],
                            "generic": "",
                            "nullable": false,
                            "union": false,
                            "idl_type": "DOMString"
                        },
                        "default": null,
                        "optional": false,
                        "variadic": false
                    }
                ],
                "ext_attrs": [],
                "special": ""
            }
        ],
        "ext_attrs": [],
        "partial": false
    }
]
```

## Documentation

**See** [original parser](https://github.com/w3c/webidl2.js)

## Contributing

Any help is welcome and appreciated.

## License

*pywebidl2* is licensed under the terms of the MIT License (see the file LICENSE).