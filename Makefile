SHELL := /bin/sh

OUTPUT_DIR ?= output
PANDOC ?= pandoc
PDF_ENGINE ?= weasyprint
PDF_CSS ?= styles/pdf.css
PANDOC_FLAGS ?= --standalone --from=gfm+smart --pdf-engine=$(PDF_ENGINE) --pdf-engine-opt=--presentational-hints --css=$(PDF_CSS)
PANDOC_LANG ?= en-US
PANDOC_FILTERS ?=
PYTHON ?= python3
MKDOCS ?= mkdocs

# Space-separated Markdown source patterns to render into PDF.
PDF_SOURCE_PATTERNS ?= \
	doc/normative/20-vision/pl/*.md \
	doc/normative/20-vision/en/*.md \
	doc/normative/25-ai-manifesto/pl/*.md \
	doc/normative/25-ai-manifesto/en/*.md \
	doc/normative/30-core-values/pl/*.md \
	doc/normative/30-core-values/en/*.md \
	doc/normative/40-constitution/pl/*.md \
	doc/normative/40-constitution/en/*.md \
	doc/normative/50-constitutional-ops/pl/*.md \
	doc/normative/50-constitutional-ops/en/*.md \

PDF_SOURCES := $(sort $(foreach pattern,$(PDF_SOURCE_PATTERNS),$(wildcard $(pattern))))
PDF_OUTPUTS := $(patsubst %.md,$(OUTPUT_DIR)/%.pdf,$(PDF_SOURCES))

.PHONY: check-json-syntax validate-schemas output output-list output-clean output-one schema-docs coverage-docs docs-gen site-docs i18n-docs html html-dev html-serve html-dev-serve html-i18n html-i18n-serve

check-json-syntax:
	./scripts/validate-json-schemas.sh --syntax-only

validate-schemas:
	./scripts/validate-json-schemas.sh

schema-docs:
	$(PYTHON) ./scripts/generate-schema-docs.py

coverage-docs:
	$(PYTHON) ./scripts/generate-workflow-coverage.py

docs-gen: schema-docs coverage-docs

site-docs: docs-gen
	$(PYTHON) ./scripts/build-site-docs.py

i18n-docs: docs-gen
	$(PYTHON) ./scripts/build-i18n-docs.py

html: html-dev

html-dev: site-docs
	@command -v "$(MKDOCS)" >/dev/null 2>&1 || { \
		echo "Missing mkdocs. Install mkdocs and mkdocs-material to build HTML." >&2; \
		exit 1; \
	}
	$(MKDOCS) build -f mkdocs.yml

html-serve: html-dev-serve

html-dev-serve: site-docs
	@command -v "$(MKDOCS)" >/dev/null 2>&1 || { \
		echo "Missing mkdocs. Install mkdocs and mkdocs-material to serve HTML." >&2; \
		exit 1; \
	}
	$(MKDOCS) serve -f mkdocs.yml

html-i18n: i18n-docs
	@command -v "$(MKDOCS)" >/dev/null 2>&1 || { \
		echo "Missing mkdocs. Install mkdocs, mkdocs-material, and mkdocs-static-i18n to build multilingual HTML." >&2; \
		exit 1; \
	}
	$(MKDOCS) build -f mkdocs.i18n.yml

html-i18n-serve: i18n-docs
	@command -v "$(MKDOCS)" >/dev/null 2>&1 || { \
		echo "Missing mkdocs. Install mkdocs, mkdocs-material, and mkdocs-static-i18n to serve multilingual HTML." >&2; \
		exit 1; \
	}
	$(MKDOCS) serve -f mkdocs.i18n.yml

output: $(PDF_OUTPUTS)

output-list:
	@printf '%s\n' $(PDF_OUTPUTS)

output-one:
	@test -n "$(FILE)" || { echo "Usage: make output-one FILE=path/to/file.md" >&2; exit 1; }
	@test -f "$(FILE)" || { echo "Missing source file: $(FILE)" >&2; exit 1; }
	@case "$(FILE)" in \
		*.md) ;; \
		*) echo "FILE must point to a Markdown source (*.md): $(FILE)" >&2; exit 1 ;; \
	esac
	@$(MAKE) "$(patsubst %.md,$(OUTPUT_DIR)/%.pdf,$(FILE))"

output-clean:
	@if [ -d "$(OUTPUT_DIR)" ]; then \
		find "$(OUTPUT_DIR)" -type f ! -name '.gitkeep' -delete; \
		find "$(OUTPUT_DIR)" -depth -type d ! -path "$(OUTPUT_DIR)" -empty -delete; \
	fi

$(OUTPUT_DIR)/%.pdf: %.md $(PDF_CSS)
	@mkdir -p "$(dir $@)"
	$(PANDOC) $(PANDOC_FLAGS) $(PANDOC_FILTERS) --metadata=lang:$(PANDOC_LANG) -o "$@" "$<"

$(OUTPUT_DIR)/%.pl.pdf: PANDOC_LANG = pl-PL
$(OUTPUT_DIR)/%.en.pdf: PANDOC_LANG = en-US
$(OUTPUT_DIR)/%.pl.pdf: PANDOC_FILTERS = --lua-filter=styles/polish-typography.lua
