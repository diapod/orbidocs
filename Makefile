SHELL := /bin/sh

.PHONY: check-json-syntax validate-schemas

check-json-syntax:
	./scripts/validate-json-schemas.sh --syntax-only

validate-schemas:
	./scripts/validate-json-schemas.sh
