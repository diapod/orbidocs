SHELL := /bin/sh

OUTPUT_DIR ?= output
PANDOC ?= pandoc
PDF_ENGINE ?= weasyprint
PDF_CSS ?= styles/pdf.css
PANDOC_FLAGS ?= --standalone --from=gfm+smart --pdf-engine=$(PDF_ENGINE) --css=$(PDF_CSS)

# Space-separated Markdown source patterns to render into PDF.
PDF_SOURCE_PATTERNS ?= \
	AI-MANIFESTO*.md \
	CONSTITUTION*.md \
	core-values/CORE-VALUES*.md \
	constitutional-ops/pl/*.md \
	constitutional-ops/en/*.md \
	README.md

PDF_SOURCES := $(sort $(foreach pattern,$(PDF_SOURCE_PATTERNS),$(wildcard $(pattern))))
PDF_OUTPUTS := $(patsubst %.md,$(OUTPUT_DIR)/%.pdf,$(PDF_SOURCES))

.PHONY: check-json-syntax validate-schemas output output-list output-clean output-one

check-json-syntax:
	./scripts/validate-json-schemas.sh --syntax-only

validate-schemas:
	./scripts/validate-json-schemas.sh

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
	$(PANDOC) $(PANDOC_FLAGS) -o "$@" "$<"
