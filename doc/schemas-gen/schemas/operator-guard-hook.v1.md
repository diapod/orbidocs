# Operator Guard Hook V1

Source schema: [`doc/schemas/operator-guard-hook.v1.schema.json`](../../schemas/operator-guard-hook.v1.schema.json)

Signed local binding of one monotonic guard declaration to a registered host admission anchor.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-guard-hook.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`guard/ref`](#field-guard-ref) | `yes` | string |  |
| [`revision/no`](#field-revision-no) | `yes` | integer |  |
| [`anchor`](#field-anchor) | `yes` | enum: `nse-decision-admission`, `package-activation`, `capability-use`, `sensorium-actuation`, `agent-effect-admission` |  |
| [`operation`](#field-operation) | `yes` | enum: `restrict`, `narrow`, `raise-risk` |  |
| [`axis`](#field-axis) | `yes` | enum: `candidate-set`, `budget`, `classification`, `operational-class`, `output-schema`, `grant-set` |  |
| [`priority`](#field-priority) | `yes` | integer |  |
| [`producer/ref`](#field-producer-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`producer/digest`](#field-producer-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | string |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-guard-hook.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-guard-ref"></a>
## `guard/ref`

- Required: `yes`
- Shape: string

<a id="field-revision-no"></a>
## `revision/no`

- Required: `yes`
- Shape: integer

<a id="field-anchor"></a>
## `anchor`

- Required: `yes`
- Shape: enum: `nse-decision-admission`, `package-activation`, `capability-use`, `sensorium-actuation`, `agent-effect-admission`

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: enum: `restrict`, `narrow`, `raise-risk`

<a id="field-axis"></a>
## `axis`

- Required: `yes`
- Shape: enum: `candidate-set`, `budget`, `classification`, `operational-class`, `output-schema`, `grant-set`

<a id="field-priority"></a>
## `priority`

- Required: `yes`
- Shape: integer

<a id="field-producer-ref"></a>
## `producer/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-producer-digest"></a>
## `producer/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
