# Causal Context v1

Source schema: [`doc/schemas/causal-context.v1.schema.json`](../../schemas/causal-context.v1.schema.json)

Portable host-derived causal metadata for one operation. It is evidence, not authority.

## Governing Basis

- [`doc/project/40-proposals/081-horizontal-protocol-primitives.md`](../../project/40-proposals/081-horizontal-protocol-primitives.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `causal-context.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`context/id`](#field-context-id) | `yes` | string |  |
| [`correlation/id`](#field-correlation-id) | `yes` | string |  |
| [`operation/id`](#field-operation-id) | `yes` | string |  |
| [`parent/operation-id`](#field-parent-operation-id) | `no` | string |  |
| [`causation/refs`](#field-causation-refs) | `yes` | array |  |
| [`origin/actor-ref`](#field-origin-actor-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`diagnostic/idempotency-digest`](#field-diagnostic-idempotency-digest) | `no` | ref: `#/$defs/sha256_digest` |  |
| [`classification/ref`](#field-classification-ref) | `no` | ref: `#/$defs/ref` |  |
| [`created/at`](#field-created-at) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`sha256_digest`](#def-sha256-digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `causal-context.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-context-id"></a>
## `context/id`

- Required: `yes`
- Shape: string

<a id="field-correlation-id"></a>
## `correlation/id`

- Required: `yes`
- Shape: string

<a id="field-operation-id"></a>
## `operation/id`

- Required: `yes`
- Shape: string

<a id="field-parent-operation-id"></a>
## `parent/operation-id`

- Required: `no`
- Shape: string

<a id="field-causation-refs"></a>
## `causation/refs`

- Required: `yes`
- Shape: array

<a id="field-origin-actor-ref"></a>
## `origin/actor-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-diagnostic-idempotency-digest"></a>
## `diagnostic/idempotency-digest`

- Required: `no`
- Shape: ref: `#/$defs/sha256_digest`

<a id="field-classification-ref"></a>
## `classification/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-created-at"></a>
## `created/at`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-sha256-digest"></a>
## `$defs.sha256_digest`

- Shape: string
