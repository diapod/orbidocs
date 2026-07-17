# Room Relay Endpoint v1

Source schema: [`doc/schemas/room-relay-endpoint.v1.schema.json`](../../schemas/room-relay-endpoint.v1.schema.json)

Durable, Agora-signed selection fact for a member-visible Room WSS relay. The fact carries no live payload and grants no authority by itself.

## Governing Basis

- [`P070`](../../project/40-proposals/070-room-primitive.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`room/id`](#field-room-id) | `yes` | ref: `room.v1.schema.json#/$defs/room_id` |  |
| [`seq/no`](#field-seq-no) | `yes` | integer |  |
| [`relay/epoch`](#field-relay-epoch) | `yes` | integer |  |
| [`relay/subject`](#field-relay-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`relay/placement`](#field-relay-placement) | `yes` | enum: `requester`, `room-member`, `federation-service` |  |
| [`endpoint/url`](#field-endpoint-url) | `yes` | string |  |
| [`crypto/profile`](#field-crypto-profile) | `yes` | const: `member-visible-tls-v1` |  |
| [`ordering/profile`](#field-ordering-profile) | `yes` | const: `relay-total-order-v1` |  |
| [`selection/evidence-refs`](#field-selection-evidence-refs) | `yes` | array |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`authority/subject`](#field-authority-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
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

<a id="field-seq-no"></a>
## `seq/no`

- Required: `yes`
- Shape: integer

<a id="field-relay-epoch"></a>
## `relay/epoch`

- Required: `yes`
- Shape: integer

<a id="field-relay-subject"></a>
## `relay/subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-relay-placement"></a>
## `relay/placement`

- Required: `yes`
- Shape: enum: `requester`, `room-member`, `federation-service`

<a id="field-endpoint-url"></a>
## `endpoint/url`

- Required: `yes`
- Shape: string

<a id="field-crypto-profile"></a>
## `crypto/profile`

- Required: `yes`
- Shape: const: `member-visible-tls-v1`

<a id="field-ordering-profile"></a>
## `ordering/profile`

- Required: `yes`
- Shape: const: `relay-total-order-v1`

<a id="field-selection-evidence-refs"></a>
## `selection/evidence-refs`

- Required: `yes`
- Shape: array

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

<a id="field-authority-subject"></a>
## `authority/subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-extensions"></a>
## `extensions`

- Required: `no`
- Shape: ref: `room.v1.schema.json#/$defs/extensions`
