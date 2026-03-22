# Distributed Intelligence Agency Documentation

[![Orbidocs Schema Validation](https://github.com/diapod/orbidocs/actions/workflows/orbidocs-schema-validation.yml/badge.svg?branch=main)](https://github.com/diapod/orbidocs/actions/workflows/orbidocs-schema-validation.yml)

## Brand Identity

- Umbrella project / organization: **Distributed Intelligence Agency**
- System and protocol family: **Orbiplex**
- Website: https://distributed-intelligence.agency/
- Contact: team@distributed-intelligence.agency
- GitHub organization: https://github.com/orgs/diapod/

## Repository Layout

The canonical documentation tree now lives under `doc/` and is divided first by
main domain, then by workflow position inside that domain.

### Domains

- `doc/normative/` – vision, values, constitution, and constitutional operational acts.
- `doc/project/` – challenges, memos, stories, proposals, requirements, and solutions.
- `doc/schemas/` – canonical machine-readable schemas and example artifacts.
- `doc/schemas-gen/` – generated human-facing schema pages and schema index.

### Normative workflow

`ideas -> vision -> core-values -> constitution -> constitutional-ops -> schemas`

Canonical positions:

- `doc/normative/10-ideas/`
- `doc/normative/20-vision/`
- `doc/normative/25-ai-manifesto/`
- `doc/normative/30-core-values/`
- `doc/normative/40-constitution/`
- `doc/normative/50-constitutional-ops/`

### Project workflow

`challenges -> memos -> stories -> proposals -> requirements -> solutions -> schemas`

Canonical positions:

- `doc/project/10-challenges/`
- `doc/project/20-memos/`
- `doc/project/30-stories/`
- `doc/project/40-proposals/`
- `doc/project/50-requirements/`
- `doc/project/60-solutions/`

Project workflow stays subordinate to the normative one. If a project document starts
governing authority, identity, sanctions, disclosure, exceptions, or other high-stakes
social rules, it should be promoted into `doc/normative/40-constitution/` or
`doc/normative/50-constitutional-ops/`.

## Key Repository Files

- `README.md` – repository entry point.
- `AGENTS.md` – guidance for documentation agents.
- `DOCS-I18N.md` – locale-detection and normalization rules.
- `TRACEABILITY.md` – linking convention across workflows and schema semantics.
- `Makefile` – schema validation, schema doc generation, PDF rendering, and HTML builds.
- `mkdocs.yml` – single-site HTML build config.
- `mkdocs.i18n.yml` – multilingual MkDocs config.
- `scripts/validate-json-schemas.sh` – schema/example validator wrapper.
- `scripts/generate-schema-docs.py` – generator for human-facing schema pages.
- `scripts/build-i18n-docs.py` – staging-tree normalizer for multilingual HTML builds.

## Schemas

Canonical schemas live in `doc/schemas/`.

Representative files:

- `doc/schemas/transcript-segment.v1.schema.json`
- `doc/schemas/transcript-bundle.v1.schema.json`
- `doc/schemas/answer-room-metadata.v1.schema.json`
- `doc/schemas/signal-marker.v1.schema.json`
- `doc/schemas/signal-transform-event.v1.schema.json`
- `doc/schemas/proof-of-personhood-attestation.v1.schema.json`
- `doc/schemas/ubc-allocation.v1.schema.json`
- `doc/schemas/ubc-settlement.v1.schema.json`
- `doc/schemas/examples/`
- `doc/schemas/examples/invalid/`
- `doc/schemas/README.md`
- `doc/schemas-gen/schema-index.md`
- `doc/schemas-gen/schemas/*.md`

## Build and Validation

### JSON Schema syntax only

```sh
make check-json-syntax
```

### Full schema validation

```sh
make validate-schemas
```

### Regenerate human-facing schema pages

```sh
make schema-docs
```

### Normalize multilingual docs tree

```sh
make i18n-docs
```

### Build single HTML site

```sh
make html
```

### Build multilingual HTML site

```sh
make html-i18n
```

### Build PDF artifacts

```sh
make output
```

## Traceability Summary

The repository uses a stratified traceability model.

### Normative path

`doc/normative/30-core-values -> doc/normative/40-constitution -> doc/normative/50-constitutional-ops -> doc/schemas-gen -> doc/schemas`

### Project path

`doc/project/10-challenges -> doc/project/20-memos -> doc/project/30-stories -> doc/project/40-proposals -> doc/project/50-requirements -> doc/schemas`

These paths are intentionally not symmetric. Normative documents carry legitimacy and
constraints. Project documents explore, narrow, and operationalize design choices. Both
meet in data contracts under `doc/schemas/`.
