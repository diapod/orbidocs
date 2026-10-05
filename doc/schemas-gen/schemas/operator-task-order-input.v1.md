# Operator Task Order Input v1

Source schema: [`doc/schemas/operator-task-order-input.v1.schema.json`](../../schemas/operator-task-order-input.v1.schema.json)

An ordinary service-order's inert input for a bounded task-pack order. Selects the exact signed offer and task profile, never local authority. Dator additionally limits question/text to 8192 UTF-8 bytes. The provider operator explicitly links the retained order to a provider-owned local round; admission grants neither a loop nor HIL.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-order-input.v1` |  |
| [`task-profile/ref`](#field-task-profile-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/offerTaskProfile/properties/task-profile~1ref` |  |
| [`task-profile/digest`](#field-task-profile-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`selected-offer/digest`](#field-selected-offer-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` | JCS v1 digest of the complete selected signed Service Offer, including its signature. |
| [`question/text`](#field-question-text) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-order-input.v1`

<a id="field-task-profile-ref"></a>
## `task-profile/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/offerTaskProfile/properties/task-profile~1ref`

<a id="field-task-profile-digest"></a>
## `task-profile/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-selected-offer-digest"></a>
## `selected-offer/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

JCS v1 digest of the complete selected signed Service Offer, including its signature.

<a id="field-question-text"></a>
## `question/text`

- Required: `yes`
- Shape: string
