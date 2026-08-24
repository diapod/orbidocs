# Artifact Extraction Profile v1

Source schema: [`doc/schemas/artifact-extraction-profile.v1.schema.json`](../../schemas/artifact-extraction-profile.v1.schema.json)

Operator-admitted, content-neutral and offline extraction profile. The profile selects one implementation and bounds parsing and candidate output; it carries no locator, source activation, credentials, artifact authority, admission, or publication authority.

## Governing Basis

- [`doc/project/40-proposals/088-pull-based-artifact-acquisition.md`](../../project/40-proposals/088-pull-based-artifact-acquisition.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `artifact-extraction-profile.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`profile/ref`](#field-profile-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`parser/id`](#field-parser-id) | `yes` | string |  |
| [`implementation/digest`](#field-implementation-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`carrier/content-types`](#field-carrier-content-types) | `yes` | array |  |
| [`selector/kinds`](#field-selector-kinds) | `yes` | array |  |
| [`candidate/framing`](#field-candidate-framing) | `yes` | enum: `portable-package`, `orbiplex-armored-package:v1` |  |
| [`candidate/cardinality`](#field-candidate-cardinality) | `yes` | enum: `exact-one`, `bounded-many` |  |
| [`limits`](#field-limits) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `artifact-extraction-profile.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-profile-ref"></a>
## `profile/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-parser-id"></a>
## `parser/id`

- Required: `yes`
- Shape: string

<a id="field-implementation-digest"></a>
## `implementation/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-carrier-content-types"></a>
## `carrier/content-types`

- Required: `yes`
- Shape: array

<a id="field-selector-kinds"></a>
## `selector/kinds`

- Required: `yes`
- Shape: array

<a id="field-candidate-framing"></a>
## `candidate/framing`

- Required: `yes`
- Shape: enum: `portable-package`, `orbiplex-armored-package:v1`

<a id="field-candidate-cardinality"></a>
## `candidate/cardinality`

- Required: `yes`
- Shape: enum: `exact-one`, `bounded-many`

<a id="field-limits"></a>
## `limits`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
