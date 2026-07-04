# Weak Signal Finding v1

Source schema: [`doc/schemas/weak-signal-finding.v1.schema.json`](../../schemas/weak-signal-finding.v1.schema.json)

Candidate weak-signal finding emitted by a local Harvester and imported into node review. This is not a publication artifact and does not authorize Whisper publication by itself.

## Governing Basis

- [`doc/project/20-memos/orbiplex-whisper.md`](../../project/20-memos/orbiplex-whisper.md)
- [`doc/project/20-memos/orbiplex-monus.md`](../../project/20-memos/orbiplex-monus.md)
- [`doc/project/40-proposals/078-weak-signal-harvester.md`](../../project/40-proposals/078-weak-signal-harvester.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)

### Stories

- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `weak-signal-finding.v1` |  |
| [`finding/id`](#field-finding-id) | `yes` | string |  |
| [`created/at`](#field-created-at) | `yes` | string |  |
| [`source/classes`](#field-source-classes) | `yes` | array |  |
| [`signal/polarity`](#field-signal-polarity) | `no` | enum: `problem`, `idea`, `question`, `context`, `mixed` |  |
| [`topic/class`](#field-topic-class) | `no` | string |  |
| [`finding/summary`](#field-finding-summary) | `yes` | string |  |
| [`finding/confidence`](#field-finding-confidence) | `yes` | enum: `low`, `medium`, `high` |  |
| [`finding/group-key`](#field-finding-group-key) | `yes` | string |  |
| [`finding/supersedes`](#field-finding-supersedes) | `no` | array |  |
| [`source/refs`](#field-source-refs) | `yes` | array |  |
| [`privacy/review-required`](#field-privacy-review-required) | `yes` | const: `True` |  |
| [`privacy/flags`](#field-privacy-flags) | `no` | array |  |
| [`suggested/actions`](#field-suggested-actions) | `yes` | array |  |
| [`harvester/ref`](#field-harvester-ref) | `no` | string |  |
| [`metadata`](#field-metadata) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`source_ref`](#def-source-ref) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `weak-signal-finding.v1`

<a id="field-finding-id"></a>
## `finding/id`

- Required: `yes`
- Shape: string

<a id="field-created-at"></a>
## `created/at`

- Required: `yes`
- Shape: string

<a id="field-source-classes"></a>
## `source/classes`

- Required: `yes`
- Shape: array

<a id="field-signal-polarity"></a>
## `signal/polarity`

- Required: `no`
- Shape: enum: `problem`, `idea`, `question`, `context`, `mixed`

<a id="field-topic-class"></a>
## `topic/class`

- Required: `no`
- Shape: string

<a id="field-finding-summary"></a>
## `finding/summary`

- Required: `yes`
- Shape: string

<a id="field-finding-confidence"></a>
## `finding/confidence`

- Required: `yes`
- Shape: enum: `low`, `medium`, `high`

<a id="field-finding-group-key"></a>
## `finding/group-key`

- Required: `yes`
- Shape: string

<a id="field-finding-supersedes"></a>
## `finding/supersedes`

- Required: `no`
- Shape: array

<a id="field-source-refs"></a>
## `source/refs`

- Required: `yes`
- Shape: array

<a id="field-privacy-review-required"></a>
## `privacy/review-required`

- Required: `yes`
- Shape: const: `True`

<a id="field-privacy-flags"></a>
## `privacy/flags`

- Required: `no`
- Shape: array

<a id="field-suggested-actions"></a>
## `suggested/actions`

- Required: `yes`
- Shape: array

<a id="field-harvester-ref"></a>
## `harvester/ref`

- Required: `no`
- Shape: string

<a id="field-metadata"></a>
## `metadata`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-source-ref"></a>
## `$defs.source_ref`

- Shape: object
