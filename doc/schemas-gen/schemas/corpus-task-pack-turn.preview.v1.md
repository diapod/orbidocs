# Corpus-task-pack-turn.preview.v1

Source schema: [`doc/schemas/corpus-task-pack-turn.preview.v1.schema.json`](../../schemas/corpus-task-pack-turn.preview.v1.schema.json)

Immutable exact review of operator choices and owner facts. preview/digest is JCS SHA-256 over this object without preview/ref and preview/digest; preview/ref is corpus-task-pack-turn:<digest>. Runtime checks equality, positive validity no longer than 300 seconds, and the Room expiry ceiling. These times bound approval, not an inference turn. Pins are observations, not authority; every mutation must resolve current owners.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-turn.preview.v1` |  |
| [`preview/ref`](#field-preview-ref) | `yes` | string |  |
| [`preview/digest`](#field-preview-digest) | `yes` | ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/digest` |  |
| [`choices`](#field-choices) | `yes` | ref: `corpus-task-pack-turn.prepare.request.v1.schema.json` |  |
| [`pins`](#field-pins) | `yes` | ref: `#/$defs/pins` |  |
| [`planned`](#field-planned) | `yes` | ref: `#/$defs/planned` |  |
| [`prepared/at`](#field-prepared-at) | `yes` | string |  |
| [`valid/until`](#field-valid-until) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`pins`](#def-pins) | object |  |
| [`planned`](#def-planned) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-turn.preview.v1`

<a id="field-preview-ref"></a>
## `preview/ref`

- Required: `yes`
- Shape: string

<a id="field-preview-digest"></a>
## `preview/digest`

- Required: `yes`
- Shape: ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/digest`

<a id="field-choices"></a>
## `choices`

- Required: `yes`
- Shape: ref: `corpus-task-pack-turn.prepare.request.v1.schema.json`

<a id="field-pins"></a>
## `pins`

- Required: `yes`
- Shape: ref: `#/$defs/pins`

<a id="field-planned"></a>
## `planned`

- Required: `yes`
- Shape: ref: `#/$defs/planned`

<a id="field-prepared-at"></a>
## `prepared/at`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid/until`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-pins"></a>
## `$defs.pins`

- Shape: object

<a id="def-planned"></a>
## `$defs.planned`

- Shape: object
