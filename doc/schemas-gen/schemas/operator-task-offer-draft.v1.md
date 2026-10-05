# Operator Task Offer Draft v1

Source schema: [`doc/schemas/operator-task-offer-draft.v1.schema.json`](../../schemas/operator-task-offer-draft.v1.schema.json)

Unsigned, non-public exact draft. Dator resolves named configuration policies; the host pins their values and digests together with the local binding, activation and exact unsigned ordinary Service Offer. Only explicit approval of this retained draft may request publication. Descriptive terms confer no operator, VM or HIL authority.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-offer-draft.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`draft/ref`](#field-draft-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`task-profile/ref`](#field-task-profile-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`task-profile/digest`](#field-task-profile-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`service/type`](#field-service-type) | `yes` | string |  |
| [`offer-template/ref`](#field-offer-template-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`offer-template/digest`](#field-offer-template-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`topics`](#field-topics) | `yes` | array |  |
| [`provider/participant-ref`](#field-provider-participant-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`price-policy/ref`](#field-price-policy-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`availability-policy/ref`](#field-availability-policy-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`local-binding/digest`](#field-local-binding-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`activation/generation`](#field-activation-generation) | `yes` | integer |  |
| [`price-policy/digest`](#field-price-policy-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`availability-policy/digest`](#field-availability-policy-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`price-policy/value`](#field-price-policy-value) | `yes` | object |  |
| [`availability-policy/value`](#field-availability-policy-value) | `yes` | object |  |
| [`offer/content`](#field-offer-content) | `yes` | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-offer-draft.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-draft-ref"></a>
## `draft/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-task-profile-ref"></a>
## `task-profile/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-task-profile-digest"></a>
## `task-profile/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-service-type"></a>
## `service/type`

- Required: `yes`
- Shape: string

<a id="field-offer-template-ref"></a>
## `offer-template/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-offer-template-digest"></a>
## `offer-template/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-topics"></a>
## `topics`

- Required: `yes`
- Shape: array

<a id="field-provider-participant-ref"></a>
## `provider/participant-ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-price-policy-ref"></a>
## `price-policy/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-availability-policy-ref"></a>
## `availability-policy/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-local-binding-digest"></a>
## `local-binding/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-activation-generation"></a>
## `activation/generation`

- Required: `yes`
- Shape: integer

<a id="field-price-policy-digest"></a>
## `price-policy/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-availability-policy-digest"></a>
## `availability-policy/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-price-policy-value"></a>
## `price-policy/value`

- Required: `yes`
- Shape: object

<a id="field-availability-policy-value"></a>
## `availability-policy/value`

- Required: `yes`
- Shape: object

<a id="field-offer-content"></a>
## `offer/content`

- Required: `yes`
- Shape: unspecified
