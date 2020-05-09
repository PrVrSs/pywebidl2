SHELL := /usr/bin/env bash
PROJECT_NAME := pywebidl2
PROJECT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/$(PROJECT_NAME)


.PHONY: unit
unit:
	pytest -v \
		-vv \
		--cov=$(PROJECT_DIR) \
		--capture=no \
		--cov-report=term-missing \
 		--cov-config=.coveragerc \

.PHONY: mypy
mypy:
	mypy $(PROJECT_DIR)

.PHONY: lint
lint:
	pylint $(PROJECT_DIR)

test: unit
