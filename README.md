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
- `doc/normative/30-core-values/`
- `doc/normative/40-constitution/`
- `doc/normative/50-constitutional-ops/`

Supplementary normative material lives outside that main workflow:

- `doc/normative/90-supplementary/`

### Project workflow

`challenges -> memos -> stories -> proposals -> requirements -> solutions -> schemas`

Canonical positions:

- `doc/project/10-challenges/`
- `doc/project/20-memos/`
- `doc/project/30-stories/`
- `doc/project/40-proposals/`
- `doc/project/50-requirements/`
- `doc/project/60-solutions/`

Within `doc/project/60-solutions/`, keep a distinction between:

- component pages such as `node.md` or `node-ui.md`,
- generated capability overviews such as `CAPABILITY-MATRIX.*.md`,
- and human-maintained contract maps such as `CAPABILITY-REGISTRY.*.md`.

`CAPABILITY-REGISTRY.*.md` is the human-facing read model for stable
`capability_id` semantics. It should be updated whenever capability ids, wire
names, semantic role boundaries, or primary runtime ownership change in `node`
or the corresponding proposals.

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
- `mkdocs.i18n.yml` – multilingual MkDocs config template.
- `mkdocs.i18n.generated.yml` – generated multilingual MkDocs config with project nav expanded from local `.nav.yml` files.
- `.github/workflows/orbidocs-pages.yml` – GitHub Pages build/deploy workflow for the `public` branch.
- `requirements-docs.txt` – Python dependencies for schema validation and MkDocs builds in CI.
- `scripts/validate-json-schemas.sh` – schema/example validator wrapper.
- `scripts/check-capability-registry.py` – verifies that `CAPABILITY-REGISTRY.*.md` matches the runtime capability map in `../node/capability/src/lib.rs`.
- `scripts/generate-schema-docs.py` – generator for human-facing schema pages.
- `scripts/generate-workflow-coverage.py` – generator for workflow coverage overview.
- `scripts/build-site-docs.py` – staging-tree normalizer for the developer HTML build.
- `scripts/build-i18n-docs.py` – staging-tree normalizer for multilingual HTML builds and generator of `mkdocs.i18n.generated.yml`.

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

### Capability registry consistency

```sh
make check-capability-registry
```

### Regenerate human-facing schema pages

```sh
make schema-docs
```

### Normalize multilingual docs tree

```sh
make i18n-docs
```

### Build developer HTML site

```sh
make html-dev
```

### Build multilingual HTML site

```sh
make html-i18n
```

### Compatibility alias

```sh
make html
```

`html` remains as a compatibility alias for `html-dev`. The canonical user-facing
site is `html-i18n`.

## GitHub Pages

The repository includes a GitHub Actions workflow that:

- triggers on pushes to the `public` branch,
- validates schemas,
- regenerates schema docs,
- builds the multilingual site with `make html-i18n`,
- deploys `output/html-i18n` to GitHub Pages.

For the custom domain:

- set **Pages -> Source** to `GitHub Actions`,
- set **Pages -> Custom domain** to `docs.orbiplex.ai`,
- create a DNS `CNAME` record:
  - `docs.orbiplex.ai -> diapod.github.io`
- verify the parent domain `orbiplex.ai` in GitHub to reduce takeover risk.

### Build PDF artifacts

```sh
make output
```

## Outputs

- `make html-dev`
  - developer single-site build
  - output: `output/html`
- `make html-i18n`
  - canonical multilingual build
  - output: `output/html-i18n`
- `make output`
  - PDF artifact build
  - output: `output/pdf`

## Traceability Summary

The repository uses a stratified traceability model.

### Normative path

`doc/normative/30-core-values -> doc/normative/40-constitution -> doc/normative/50-constitutional-ops -> doc/schemas-gen -> doc/schemas`

### Project path

`doc/project/10-challenges -> doc/project/20-memos -> doc/project/30-stories -> doc/project/40-proposals -> doc/project/50-requirements -> doc/schemas`

These paths are intentionally not symmetric. Normative documents carry legitimacy and
constraints. Project documents explore, narrow, and operationalize design choices. Both
meet in data contracts under `doc/schemas/`.

## Node Implementation Bridge

The closest implementation-side counterpart of the `orbidocs` solutions layer lives in:

- `../node/docs/implementation-ledger.toml`
- `../node/docs/IMPLEMENTATION-LEDGER.md`

For capability semantics specifically, also reconcile against:

- `../node/capability/src/lib.rs`
- `doc/project/60-solutions/CAPABILITY-REGISTRY.en.md`
- `doc/project/60-solutions/CAPABILITY-REGISTRY.pl.md`

This ledger is not generated from `orbidocs`. It is maintained manually in the
`node` repository and should be reconciled there against:

- `doc/project/60-solutions/*`
- `doc/schemas/*`
- and, where they introduce implementation-relevant decisions, selected project
  `proposals`, `requirements`, `stories`, and `memos`

That split is intentional:

- `orbidocs` remains the semantic and architectural source
- `node` keeps the repository-local implementation mapping, ownership, and coarse status
