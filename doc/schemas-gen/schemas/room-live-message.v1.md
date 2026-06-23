# Room Live Message v1

Source schema: [`doc/schemas/room-live-message.v1.schema.json`](../../schemas/room-live-message.v1.schema.json)

Ephemeral live-room frame. It is validated at the live transport boundary and is not a durable room fact.

## Governing Basis

- [`P070`](../../project/40-proposals/070-room-primitive.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`room/id`](#field-room-id) | `yes` | ref: `room.v1.schema.json#/$defs/room_id` |  |
| [`session/ref`](#field-session-ref) | `yes` | string |  |
| [`from/subject`](#field-from-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`seq/no`](#field-seq-no) | `yes` | integer |  |
| [`nonce`](#field-nonce) | `yes` | string | Base64url-encoded cryptographically random nonce, at least 128 bits before encoding. |
| [`size/bytes`](#field-size-bytes) | `yes` | integer |  |
| [`content/type`](#field-content-type) | `yes` | string |  |
| [`content`](#field-content) | `yes` | string |  |
| [`content/digest`](#field-content-digest) | `no` | string |  |
| [`sent-at`](#field-sent-at) | `no` | string |  |
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

<a id="field-session-ref"></a>
## `session/ref`

- Required: `yes`
- Shape: string

<a id="field-from-subject"></a>
## `from/subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-seq-no"></a>
## `seq/no`

- Required: `yes`
- Shape: integer

<a id="field-nonce"></a>
## `nonce`

- Required: `yes`
- Shape: string

Base64url-encoded cryptographically random nonce, at least 128 bits before encoding.

<a id="field-size-bytes"></a>
## `size/bytes`

- Required: `yes`
- Shape: integer

<a id="field-content-type"></a>
## `content/type`

- Required: `yes`
- Shape: string

<a id="field-content"></a>
## `content`

- Required: `yes`
- Shape: string

<a id="field-content-digest"></a>
## `content/digest`

- Required: `no`
- Shape: string

<a id="field-sent-at"></a>
## `sent-at`

- Required: `no`
- Shape: string

<a id="field-extensions"></a>
## `extensions`

- Required: `no`
- Shape: ref: `room.v1.schema.json#/$defs/extensions`
