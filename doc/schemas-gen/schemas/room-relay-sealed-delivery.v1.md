# Room Relay Sealed Delivery v1

Source schema: [`doc/schemas/room-relay-sealed-delivery.v1.schema.json`](../../schemas/room-relay-sealed-delivery.v1.schema.json)

Ephemeral sender-authenticated encrypted Room carrier frame for a non-member federation relay. The explicit delivery/kind discriminator prevents ambiguity with member-visible deliveries. The relay can validate and order the bounded envelope but cannot read the content payload.

## Governing Basis

- [`P070`](../../project/40-proposals/070-room-primitive.md)
- [`P082`](../../project/40-proposals/082-sensorium-interfaces.md)
- [`P083`](../../project/40-proposals/083-sensorium-interactive-interfaces.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`delivery/kind`](#field-delivery-kind) | `yes` | const: `sealed` |  |
| [`crypto/profile`](#field-crypto-profile) | `yes` | const: `sealed-sender-key-v1` |  |
| [`room/id`](#field-room-id) | `yes` | ref: `room.v1.schema.json#/$defs/room_id` |  |
| [`relay/epoch`](#field-relay-epoch) | `yes` | integer |  |
| [`relay/seq-no`](#field-relay-seq-no) | `yes` | integer |  |
| [`membership/epoch`](#field-membership-epoch) | `yes` | integer |  |
| [`sender/subject`](#field-sender-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`sender/seq-no`](#field-sender-seq-no) | `yes` | integer |  |
| [`nonce`](#field-nonce) | `yes` | string |  |
| [`ciphertext`](#field-ciphertext) | `yes` | string |  |
| [`ciphertext/digest`](#field-ciphertext-digest) | `yes` | string |  |
| [`signer/ref`](#field-signer-ref) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | object |  |
| [`accepted-at`](#field-accepted-at) | `yes` | string |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-delivery-kind"></a>
## `delivery/kind`

- Required: `yes`
- Shape: const: `sealed`

<a id="field-crypto-profile"></a>
## `crypto/profile`

- Required: `yes`
- Shape: const: `sealed-sender-key-v1`

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/room_id`

<a id="field-relay-epoch"></a>
## `relay/epoch`

- Required: `yes`
- Shape: integer

<a id="field-relay-seq-no"></a>
## `relay/seq-no`

- Required: `yes`
- Shape: integer

<a id="field-membership-epoch"></a>
## `membership/epoch`

- Required: `yes`
- Shape: integer

<a id="field-sender-subject"></a>
## `sender/subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-sender-seq-no"></a>
## `sender/seq-no`

- Required: `yes`
- Shape: integer

<a id="field-nonce"></a>
## `nonce`

- Required: `yes`
- Shape: string

<a id="field-ciphertext"></a>
## `ciphertext`

- Required: `yes`
- Shape: string

<a id="field-ciphertext-digest"></a>
## `ciphertext/digest`

- Required: `yes`
- Shape: string

<a id="field-signer-ref"></a>
## `signer/ref`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object

<a id="field-accepted-at"></a>
## `accepted-at`

- Required: `yes`
- Shape: string
