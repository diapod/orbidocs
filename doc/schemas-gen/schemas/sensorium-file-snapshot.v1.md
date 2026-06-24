# Sensorium File Snapshot v1

Source schema: [`doc/schemas/sensorium-file-snapshot.v1.schema.json`](../../schemas/sensorium-file-snapshot.v1.schema.json)

Bounded file or directory metadata snapshot under an allowlisted Workbench root.

## Governing Basis

- [`doc/project/40-proposals/071-sensorium-workbench.md`](../../project/40-proposals/071-sensorium-workbench.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)
- [`doc/project/50-requirements/requirements-014-resource-opinions.md`](../../project/50-requirements/requirements-014-resource-opinions.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)
- [`doc/project/30-stories/story-008-cool-site-comment.md`](../../project/30-stories/story-008-cool-site-comment.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-file-snapshot.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`snapshot/ref`](#field-snapshot-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`address`](#field-address) | `yes` | ref: `sensorium-relative-path-address.v1.schema.json` |  |
| [`entries`](#field-entries) | `yes` | array |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`relativePath`](#def-relativepath) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-file-snapshot.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-snapshot-ref"></a>
## `snapshot/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-address"></a>
## `address`

- Required: `yes`
- Shape: ref: `sensorium-relative-path-address.v1.schema.json`

<a id="field-entries"></a>
## `entries`

- Required: `yes`
- Shape: array

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-relativepath"></a>
## `$defs.relativePath`

- Shape: string
