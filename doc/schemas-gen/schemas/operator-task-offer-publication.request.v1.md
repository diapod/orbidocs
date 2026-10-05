# Operator Task Offer Publication.request v1

Source schema: [`doc/schemas/operator-task-offer-publication.request.v1.schema.json`](../../schemas/operator-task-offer-publication.request.v1.schema.json)

Explicit current-operator approval of one retained exact draft, or withdrawal of its ordinary offer. It never accepts replacement draft or offer bytes.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-offer-publication.request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`draft/ref`](#field-draft-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`action`](#field-action) | `yes` | enum: `publish`, `withdraw` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`local-binding/expected-digest`](#field-local-binding-expected-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-offer-publication.request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-draft-ref"></a>
## `draft/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-action"></a>
## `action`

- Required: `yes`
- Shape: enum: `publish`, `withdraw`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-local-binding-expected-digest"></a>
## `local-binding/expected-digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`
