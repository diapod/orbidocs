# Domain Enum Classification v1

Source schema: [`doc/schemas/enum-classification.v1.schema.json`](../../schemas/enum-classification.v1.schema.json)

Reviewed classification of one structurally discovered domain enum.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `enum-classification.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`subject/ref`](#field-subject-ref) | `yes` | ref: `#/$defs/identifier` |  |
| [`domain`](#field-domain) | `yes` | ref: `#/$defs/identifier` |  |
| [`declaration/name`](#field-declaration-name) | `yes` | ref: `#/$defs/identifier` |  |
| [`source/locator`](#field-source-locator) | `yes` | string |  |
| [`source/fingerprint`](#field-source-fingerprint) | `yes` | ref: `#/$defs/digest` |  |
| [`disposition`](#field-disposition) | `yes` | ref: `#/$defs/disposition` |  |
| [`call-site/refs`](#field-call-site-refs) | `yes` | ref: `#/$defs/refs` |  |
| [`wire/impact`](#field-wire-impact) | `yes` | ref: `#/$defs/identifier` |  |
| [`capability/owner`](#field-capability-owner) | `yes` | ref: `#/$defs/identifier` |  |
| [`refusal/behavior`](#field-refusal-behavior) | `yes` | ref: `#/$defs/identifier` |  |
| [`evidence/refs`](#field-evidence-refs) | `yes` | ref: `#/$defs/refs` |  |
| [`review`](#field-review) | `yes` | ref: `#/$defs/review` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`identifier`](#def-identifier) | string |  |
| [`digest`](#def-digest) | string |  |
| [`disposition`](#def-disposition) | enum: `closed-invariant`, `configurable-subset`, `code-backed-registry-candidate`, `unclassified` |  |
| [`refs`](#def-refs) | array |  |
| [`review`](#def-review) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `enum-classification.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-subject-ref"></a>
## `subject/ref`

- Required: `yes`
- Shape: ref: `#/$defs/identifier`

<a id="field-domain"></a>
## `domain`

- Required: `yes`
- Shape: ref: `#/$defs/identifier`

<a id="field-declaration-name"></a>
## `declaration/name`

- Required: `yes`
- Shape: ref: `#/$defs/identifier`

<a id="field-source-locator"></a>
## `source/locator`

- Required: `yes`
- Shape: string

<a id="field-source-fingerprint"></a>
## `source/fingerprint`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-disposition"></a>
## `disposition`

- Required: `yes`
- Shape: ref: `#/$defs/disposition`

<a id="field-call-site-refs"></a>
## `call-site/refs`

- Required: `yes`
- Shape: ref: `#/$defs/refs`

<a id="field-wire-impact"></a>
## `wire/impact`

- Required: `yes`
- Shape: ref: `#/$defs/identifier`

<a id="field-capability-owner"></a>
## `capability/owner`

- Required: `yes`
- Shape: ref: `#/$defs/identifier`

<a id="field-refusal-behavior"></a>
## `refusal/behavior`

- Required: `yes`
- Shape: ref: `#/$defs/identifier`

<a id="field-evidence-refs"></a>
## `evidence/refs`

- Required: `yes`
- Shape: ref: `#/$defs/refs`

<a id="field-review"></a>
## `review`

- Required: `yes`
- Shape: ref: `#/$defs/review`

## Definition Semantics

<a id="def-identifier"></a>
## `$defs.identifier`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-disposition"></a>
## `$defs.disposition`

- Shape: enum: `closed-invariant`, `configurable-subset`, `code-backed-registry-candidate`, `unclassified`

<a id="def-refs"></a>
## `$defs.refs`

- Shape: array

<a id="def-review"></a>
## `$defs.review`

- Shape: object
