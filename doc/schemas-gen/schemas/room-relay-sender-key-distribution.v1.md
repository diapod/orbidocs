# Room Relay Sender Key Distribution v1

Source schema: [`doc/schemas/room-relay-sender-key-distribution.v1.schema.json`](../../schemas/room-relay-sender-key-distribution.v1.schema.json)

Pairwise sealed and sender-authenticated distribution of one Room relay sender key. This artifact is recipient-private and MUST NOT be routed through or retained by the federation relay.

## Governing Basis

- [`P070`](../../project/40-proposals/070-room-primitive.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`room/id`](#field-room-id) | `yes` | ref: `room.v1.schema.json#/$defs/room_id` |  |
| [`relay/epoch`](#field-relay-epoch) | `yes` | integer |  |
| [`membership/epoch`](#field-membership-epoch) | `yes` | integer |  |
| [`sender/subject`](#field-sender-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`recipient/subject`](#field-recipient-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`sender/ephemeral-pub`](#field-sender-ephemeral-pub) | `yes` | string |  |
| [`nonce`](#field-nonce) | `yes` | string |  |
| [`ciphertext`](#field-ciphertext) | `yes` | string |  |
| [`ciphertext/digest`](#field-ciphertext-digest) | `yes` | string |  |
| [`signer/ref`](#field-signer-ref) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/room_id`

<a id="field-relay-epoch"></a>
## `relay/epoch`

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

<a id="field-recipient-subject"></a>
## `recipient/subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-sender-ephemeral-pub"></a>
## `sender/ephemeral-pub`

- Required: `yes`
- Shape: string

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
