# Local Capability Catalog Result v1

Source schema: [`doc/schemas/capability-catalog-result.v1.schema.json`](../../schemas/capability-catalog-result.v1.schema.json)

Caller-scoped, lower-trust catalog data. Presence and readiness do not authorize execution.

## Governing Basis

- [`doc/project/40-proposals/072-capability-registry.md`](../../project/40-proposals/072-capability-registry.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `capability-catalog-result.v1` |  |
| [`operation`](#field-operation) | `yes` | enum: `list`, `describe` |  |
| [`state`](#field-state) | `yes` | enum: `ok`, `described`, `ambiguous-contract`, `unresolved-contract`, `not-found`, `stale-cursor`, `denied` |  |
| [`catalog/revision`](#field-catalog-revision) | `yes` | string |  |
| [`classification/tier`](#field-classification-tier) | `yes` | enum: `Public`, `Community`, `Personal` |  |
| [`items`](#field-items) | `no` | array |  |
| [`next/cursor`](#field-next-cursor) | `no` | string |  |
| [`capability/id`](#field-capability-id) | `no` | string |  |
| [`availability`](#field-availability) | `no` | enum: `ready`, `unavailable`, `unknown` |  |
| [`authorization`](#field-authorization) | `no` | ref: `#/$defs/authorization` |  |
| [`operations`](#field-operations) | `no` | array |  |
| [`guidance`](#field-guidance) | `no` | ref: `capability-guidance.v1.schema.json` |  |
| [`guidance/digest`](#field-guidance-digest) | `no` | string |  |
| [`source/digest`](#field-source-digest) | `no` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`item`](#def-item) | object |  |
| [`authorization`](#def-authorization) | object |  |
| [`binding`](#def-binding) | object |  |
| [`operation`](#def-operation) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-catalog-result.v1`

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: enum: `list`, `describe`

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `ok`, `described`, `ambiguous-contract`, `unresolved-contract`, `not-found`, `stale-cursor`, `denied`

<a id="field-catalog-revision"></a>
## `catalog/revision`

- Required: `yes`
- Shape: string

<a id="field-classification-tier"></a>
## `classification/tier`

- Required: `yes`
- Shape: enum: `Public`, `Community`, `Personal`

<a id="field-items"></a>
## `items`

- Required: `no`
- Shape: array

<a id="field-next-cursor"></a>
## `next/cursor`

- Required: `no`
- Shape: string

<a id="field-capability-id"></a>
## `capability/id`

- Required: `no`
- Shape: string

<a id="field-availability"></a>
## `availability`

- Required: `no`
- Shape: enum: `ready`, `unavailable`, `unknown`

<a id="field-authorization"></a>
## `authorization`

- Required: `no`
- Shape: ref: `#/$defs/authorization`

<a id="field-operations"></a>
## `operations`

- Required: `no`
- Shape: array

<a id="field-guidance"></a>
## `guidance`

- Required: `no`
- Shape: ref: `capability-guidance.v1.schema.json`

<a id="field-guidance-digest"></a>
## `guidance/digest`

- Required: `no`
- Shape: string

<a id="field-source-digest"></a>
## `source/digest`

- Required: `no`
- Shape: string

## Definition Semantics

<a id="def-item"></a>
## `$defs.item`

- Shape: object

<a id="def-authorization"></a>
## `$defs.authorization`

- Shape: object

<a id="def-binding"></a>
## `$defs.binding`

- Shape: object

<a id="def-operation"></a>
## `$defs.operation`

- Shape: object
