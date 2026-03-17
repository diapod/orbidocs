SHELL := /bin/sh

.PHONY: validate-schemas

validate-schemas:
	./scripts/validate-json-schemas.sh
