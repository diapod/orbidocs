# Package Capability Reconciliation Evidence v1

Source schema: [`doc/schemas/package-capability-reconciliation-evidence.v1.schema.json`](../../schemas/package-capability-reconciliation-evidence.v1.schema.json)

Read-only provider evidence. The host separately authenticates the recorded provider and compares every invocation binding and the exact effect set. A committed effect is not a validated output; not-found and pending never prove absence.

## Governing Basis

- [`doc/project/40-proposals/093-package-scoped-private-capabilities.md`](../../project/40-proposals/093-package-scoped-private-capabilities.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `package-capability-reconciliation-evidence.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`caller`](#field-caller) | `yes` | ref: `package-capability-invocation.v1.schema.json#/properties/caller` |  |
| [`invocation/id`](#field-invocation-id) | `yes` | ref: `package-capability-invocation.v1.schema.json#/$defs/invocation-id` |  |
| [`request/digest`](#field-request-digest) | `yes` | ref: `package-capability-invocation.v1.schema.json#/$defs/digest` |  |
| [`capability/id`](#field-capability-id) | `yes` | ref: `package-capability-invocation.v1.schema.json#/$defs/capability-id` |  |
| [`contract/digest`](#field-contract-digest) | `yes` | ref: `package-capability-invocation.v1.schema.json#/$defs/digest` |  |
| [`activation/generation`](#field-activation-generation) | `yes` | integer |  |
| [`effect/refs`](#field-effect-refs) | `yes` | array |  |
| [`state`](#field-state) | `yes` | enum: `committed`, `abandoned`, `pending`, `not-found` |  |
| [`observed-at`](#field-observed-at) | `yes` | ref: `package-capability-invocation.v1.schema.json#/$defs/timestamp` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `package-capability-reconciliation-evidence.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-caller"></a>
## `caller`

- Required: `yes`
- Shape: ref: `package-capability-invocation.v1.schema.json#/properties/caller`

<a id="field-invocation-id"></a>
## `invocation/id`

- Required: `yes`
- Shape: ref: `package-capability-invocation.v1.schema.json#/$defs/invocation-id`

<a id="field-request-digest"></a>
## `request/digest`

- Required: `yes`
- Shape: ref: `package-capability-invocation.v1.schema.json#/$defs/digest`

<a id="field-capability-id"></a>
## `capability/id`

- Required: `yes`
- Shape: ref: `package-capability-invocation.v1.schema.json#/$defs/capability-id`

<a id="field-contract-digest"></a>
## `contract/digest`

- Required: `yes`
- Shape: ref: `package-capability-invocation.v1.schema.json#/$defs/digest`

<a id="field-activation-generation"></a>
## `activation/generation`

- Required: `yes`
- Shape: integer

<a id="field-effect-refs"></a>
## `effect/refs`

- Required: `yes`
- Shape: array

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `committed`, `abandoned`, `pending`, `not-found`

<a id="field-observed-at"></a>
## `observed-at`

- Required: `yes`
- Shape: ref: `package-capability-invocation.v1.schema.json#/$defs/timestamp`
