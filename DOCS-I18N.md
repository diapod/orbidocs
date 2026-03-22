# Documentation I18N Rules

This repository accepts two locale markers in source markdown files.

- language suffix in the filename:
  - `VISION.pl.md`
  - `VISION.en.md`
- language subdirectory in the path:
  - `doc/normative/20-vision/pl/VISION.pl.md`
  - `doc/normative/20-vision/en/VISION.en.md`
  - `doc/normative/50-constitutional-ops/pl/RAW-SIGNAL-POLICY.pl.md`
  - `doc/normative/50-constitutional-ops/en/RAW-SIGNAL-POLICY.en.md`

## Accepted input model

A file may declare its locale through:

1. suffix only,
2. directory only,
3. both suffix and directory.

Examples:

- valid:
  - `VISION.pl.md`
  - `doc/normative/50-constitutional-ops/pl/RAW-SIGNAL-POLICY.md`
  - `doc/normative/50-constitutional-ops/pl/RAW-SIGNAL-POLICY.pl.md`
- invalid:
  - `doc/normative/50-constitutional-ops/pl/RAW-SIGNAL-POLICY.en.md`
  - `doc/normative/50-constitutional-ops/en/RAW-SIGNAL-POLICY.pl.md`

If both signals are present, they must agree.

## Shared files

Files without locale markers are treated as shared documentation and may be copied into
both locale trees unchanged except for link normalization.

Examples:

- `README.md`
- `TRACEABILITY.md`
- `doc/project/PROJECTS.md`
- `doc/schemas/README.md`
- schema docs under `doc/schemas-gen/`

## Canonical build model

Mixed source naming is tolerated only at the source layer.

The build layer must normalize everything to a single locale model:

- `build/i18n-docs/pl/...`
- `build/i18n-docs/en/...`

Within that normalized tree:

- file names no longer carry locale suffixes,
- locale is expressed by the directory only,
- links should target canonical names such as `doc/normative/40-constitution/CONSTITUTION.md` or
  `doc/normative/50-constitutional-ops/RAW-SIGNAL-POLICY.md`.

## Resolution rule

Locale detection priority is:

1. detect suffix locale if present,
2. detect directory locale if present,
3. if both exist, require equality,
4. if neither exists, treat the file as shared.

This rule allows gradual migration without forcing an immediate source refactor while
keeping the normalized build tree unambiguous.
