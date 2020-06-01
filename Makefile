SHELL := /usr/bin/env bash

PROJECT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
ANTLR4 := java -jar antlr-4.8-complete.jar

.PHONY: unit
unit:
	poetry run pytest -v \
		-vv \
		--cov=pywebidl2 \
		--capture=no \
		--cov-report=term-missing \
 		--cov-config=.coveragerc \

.PHONY: mypy
mypy:
	poetry run mypy pywebidl2

.PHONY: lint
lint:
	poetry run pylint pywebidl2

test: lint mypy unit

.PHONY: grammar
grammar:
	$(ANTLR4) -no-listener -visitor -Dlanguage=Python3 $(PROJECT_DIR)/grammar/WebIDLParser.g4 $(PROJECT_DIR)/grammar/WebIDLLexer.g4 -o $(PROJECT_DIR)/pywebidl2/generated

