# Corpus Task-pack Candidate Adoption v1

Source schema: [`doc/schemas/corpus-task-pack-candidate-adoption.v1.schema.json`](../../schemas/corpus-task-pack-candidate-adoption.v1.schema.json)

Separate owner-signed adoption of an exact historical Solver source for fresh review in one communication epoch. Original proposal bytes, attribution, signature and expiry are preserved, not renewed. Owner admission resolves all commitments, the active epoch head and current mandate. Adoption grants no VM, effect, HIL or publication consent. A fresh review and separate Chair decision are required. Canonical carrier is bounded to 32 KiB by the core.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-candidate-adoption.v1` |  |
| [`adoption/ref`](#field-adoption-ref) | `yes` | string |  |
| [`epoch/ref`](#field-epoch-ref) | `yes` | ref: `corpus-authority-epoch.v1.schema.json#/$defs/epoch-ref` |  |
| [`context`](#field-context) | `yes` | ref: `corpus-authority-epoch.v1.schema.json#/$defs/context` |  |
| [`owner/node-id`](#field-owner-node-id) | `yes` | string |  |
| [`chair/mandate`](#field-chair-mandate) | `yes` | unspecified |  |
| [`source`](#field-source) | `yes` | ref: `#/$defs/source` |  |
| [`approved/digest`](#field-approved-digest) | `yes` | ref: `corpus-authority-epoch.v1.schema.json#/$defs/digest` |  |
| [`adopted/at`](#field-adopted-at) | `yes` | string |  |
| [`valid/until`](#field-valid-until) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `corpus-authority-epoch.v1.schema.json#/properties/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`source`](#def-source) | object |  |
| [`preview`](#def-preview) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-candidate-adoption.v1`

<a id="field-adoption-ref"></a>
## `adoption/ref`

- Required: `yes`
- Shape: string

<a id="field-epoch-ref"></a>
## `epoch/ref`

- Required: `yes`
- Shape: ref: `corpus-authority-epoch.v1.schema.json#/$defs/epoch-ref`

<a id="field-context"></a>
## `context`

- Required: `yes`
- Shape: ref: `corpus-authority-epoch.v1.schema.json#/$defs/context`

<a id="field-owner-node-id"></a>
## `owner/node-id`

- Required: `yes`
- Shape: string

<a id="field-chair-mandate"></a>
## `chair/mandate`

- Required: `yes`
- Shape: unspecified

<a id="field-source"></a>
## `source`

- Required: `yes`
- Shape: ref: `#/$defs/source`

<a id="field-approved-digest"></a>
## `approved/digest`

- Required: `yes`
- Shape: ref: `corpus-authority-epoch.v1.schema.json#/$defs/digest`

<a id="field-adopted-at"></a>
## `adopted/at`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid/until`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `corpus-authority-epoch.v1.schema.json#/properties/signature`

## Definition Semantics

<a id="def-source"></a>
## `$defs.source`

- Shape: object

<a id="def-preview"></a>
## `$defs.preview`

- Shape: object
