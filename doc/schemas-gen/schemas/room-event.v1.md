# Room Event v1

Source schema: [`doc/schemas/room-event.v1.schema.json`](../../schemas/room-event.v1.schema.json)

Durable room lifecycle or authority event payload carried by an Agora record envelope.

## Governing Basis

- [`P070`](../../project/40-proposals/070-room-primitive.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`room/id`](#field-room-id) | `yes` | ref: `room.v1.schema.json#/$defs/room_id` |  |
| [`event`](#field-event) | `yes` | enum: `opened`, `delegated`, `delegation-revoked`, `member-granted`, `member-revoked`, `ready`, `expired`, `closed` |  |
| [`authority/subject`](#field-authority-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`subject`](#field-subject) | `no` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`seq/no`](#field-seq-no) | `yes` | integer |  |
| [`created-at`](#field-created-at) | `yes` | string |  |
| [`reason/ref`](#field-reason-ref) | `no` | string |  |
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

<a id="field-event"></a>
## `event`

- Required: `yes`
- Shape: enum: `opened`, `delegated`, `delegation-revoked`, `member-granted`, `member-revoked`, `ready`, `expired`, `closed`

<a id="field-authority-subject"></a>
## `authority/subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-subject"></a>
## `subject`

- Required: `no`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-seq-no"></a>
## `seq/no`

- Required: `yes`
- Shape: integer

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

<a id="field-reason-ref"></a>
## `reason/ref`

- Required: `no`
- Shape: string

<a id="field-extensions"></a>
## `extensions`

- Required: `no`
- Shape: ref: `room.v1.schema.json#/$defs/extensions`
