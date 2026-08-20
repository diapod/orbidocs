# Corpus Turn Order Offer v1

Source schema: [`doc/schemas/corpus-turn-order-offer.v1.schema.json`](../../schemas/corpus-turn-order-offer.v1.schema.json)

Host-built immutable and target-free candidate projection for one exact Corpus Room turn.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-turn-order-offer.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`offer/ref`](#field-offer-ref) | `yes` | string |  |
| [`offer/digest`](#field-offer-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`round/id`](#field-round-id) | `yes` | string |  |
| [`turn/no`](#field-turn-no) | `yes` | integer |  |
| [`previous-floor-holder`](#field-previous-floor-holder) | `no` | ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject` |  |
| [`room-policy/ref`](#field-room-policy-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`room-policy/digest`](#field-room-policy-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`room-policy/generation`](#field-room-policy-generation) | `yes` | integer |  |
| [`chair-policy/ref`](#field-chair-policy-ref) | `yes` | string |  |
| [`chair-policy/digest`](#field-chair-policy-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`membership/high-water-seq-no`](#field-membership-high-water-seq-no) | `yes` | integer |  |
| [`sanction/high-water-seq-no`](#field-sanction-high-water-seq-no) | `yes` | integer |  |
| [`candidates`](#field-candidates) | `yes` | array |  |
| [`created-at`](#field-created-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`candidate`](#def-candidate) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-turn-order-offer.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-offer-ref"></a>
## `offer/ref`

- Required: `yes`
- Shape: string

<a id="field-offer-digest"></a>
## `offer/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: string

<a id="field-round-id"></a>
## `round/id`

- Required: `yes`
- Shape: string

<a id="field-turn-no"></a>
## `turn/no`

- Required: `yes`
- Shape: integer

<a id="field-previous-floor-holder"></a>
## `previous-floor-holder`

- Required: `no`
- Shape: ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject`

<a id="field-room-policy-ref"></a>
## `room-policy/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-room-policy-digest"></a>
## `room-policy/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-room-policy-generation"></a>
## `room-policy/generation`

- Required: `yes`
- Shape: integer

<a id="field-chair-policy-ref"></a>
## `chair-policy/ref`

- Required: `yes`
- Shape: string

<a id="field-chair-policy-digest"></a>
## `chair-policy/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-membership-high-water-seq-no"></a>
## `membership/high-water-seq-no`

- Required: `yes`
- Shape: integer

<a id="field-sanction-high-water-seq-no"></a>
## `sanction/high-water-seq-no`

- Required: `yes`
- Shape: integer

<a id="field-candidates"></a>
## `candidates`

- Required: `yes`
- Shape: array

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-candidate"></a>
## `$defs.candidate`

- Shape: object
