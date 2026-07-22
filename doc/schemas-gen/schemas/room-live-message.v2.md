# Room Live Message v2

Source schema: [`doc/schemas/room-live-message.v2.schema.json`](../../schemas/room-live-message.v2.schema.json)

Ephemeral live-room frame with stable message identity and bounded conversational reply hints.

## Governing Basis

- [`doc/project/40-proposals/070-room-primitive.md`](../../project/40-proposals/070-room-primitive.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `2` |  |
| [`room/id`](#field-room-id) | `yes` | ref: `room.v1.schema.json#/$defs/room_id` |  |
| [`from/subject`](#field-from-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`seq/no`](#field-seq-no) | `yes` | integer |  |
| [`message/ref`](#field-message-ref) | `yes` | string |  |
| [`reply/refs`](#field-reply-refs) | `no` | array |  |
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
- Shape: const: `2`

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/room_id`

<a id="field-from-subject"></a>
## `from/subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-seq-no"></a>
## `seq/no`

- Required: `yes`
- Shape: integer

<a id="field-message-ref"></a>
## `message/ref`

- Required: `yes`
- Shape: string

<a id="field-reply-refs"></a>
## `reply/refs`

- Required: `no`
- Shape: array

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
