# Room Membership Attestation v1

Source schema: [`doc/schemas/room-membership-attestation.v1.schema.json`](../../schemas/room-membership-attestation.v1.schema.json)

Short-lived signed projection answer for room membership and grant checks.

## Governing Basis

- [`P070`](../../project/40-proposals/070-room-primitive.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`room/id`](#field-room-id) | `yes` | ref: `room.v1.schema.json#/$defs/room_id` |  |
| [`subject`](#field-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`member`](#field-member) | `yes` | boolean |  |
| [`grants`](#field-grants) | `yes` | array |  |
| [`high-water/seq-no`](#field-high-water-seq-no) | `yes` | integer |  |
| [`source/refs`](#field-source-refs) | `yes` | array |  |
| [`attested-at`](#field-attested-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`signer/ref`](#field-signer-ref) | `yes` | string | Canonical Room-authority subject reference carrying one base58btc Ed25519 did:key. Runtime verification additionally checks the multicodec prefix and decoded key length. |
| [`signature`](#field-signature) | `yes` | object |  |
| [`extensions`](#field-extensions) | `no` | ref: `room.v1.schema.json#/$defs/extensions` |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/room_id`

<a id="field-subject"></a>
## `subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-member"></a>
## `member`

- Required: `yes`
- Shape: boolean

<a id="field-grants"></a>
## `grants`

- Required: `yes`
- Shape: array

<a id="field-high-water-seq-no"></a>
## `high-water/seq-no`

- Required: `yes`
- Shape: integer

<a id="field-source-refs"></a>
## `source/refs`

- Required: `yes`
- Shape: array

<a id="field-attested-at"></a>
## `attested-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

<a id="field-signer-ref"></a>
## `signer/ref`

- Required: `yes`
- Shape: string

Canonical Room-authority subject reference carrying one base58btc Ed25519 did:key. Runtime verification additionally checks the multicodec prefix and decoded key length.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object

<a id="field-extensions"></a>
## `extensions`

- Required: `no`
- Shape: ref: `room.v1.schema.json#/$defs/extensions`
