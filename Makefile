SHELL := /usr/bin/env bash

ANTLR4 := java -jar antlr-4.11.1-complete.jar
PROJECT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

.PHONY: unit
unit:
	poetry run pytest

.PHONY: mypy
mypy:
	poetry run mypy pywebidl2

.PHONY: lint
lint:
	poetry run pylint pywebidl2

.PHONY: parser
parser:
	$(ANTLR4) -no-listener \
		-visitor -Dlanguage=Python3 \
		-o $(PROJECT_DIR)/pywebidl2/generated \
		$(PROJECT_DIR)/grammar/WebIDLParser.g4 $(PROJECT_DIR)/grammar/WebIDLLexer.g4

test: lint mypy unit
