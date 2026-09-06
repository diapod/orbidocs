# Room Contribution Inference v1

Source schema: [`doc/schemas/room-contribution-inference.v1.schema.json`](../../schemas/room-contribution-inference.v1.schema.json)

Immutable content-bound contribution evidence; not membership or effect authority.

## Governing Basis

- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `room-contribution-inference.v1` |  |
| [`room/id`](#field-room-id) | `yes` | ref: `room.v1.schema.json#/$defs/room_id` |  |
| [`subject`](#field-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`message/ref`](#field-message-ref) | `yes` | ref: `room-live-message.v2.schema.json#/properties/message~1ref` |  |
| [`message/seq-no`](#field-message-seq-no) | `yes` | integer |  |
| [`content/type`](#field-content-type) | `yes` | ref: `room-live-message.v2.schema.json#/properties/content~1type` |  |
| [`content/digest`](#field-content-digest) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/digest` |  |
| [`execution/provenance`](#field-execution-provenance) | `yes` | ref: `inference-execution-provenance.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `room-contribution-inference.v1`

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/room_id`

<a id="field-subject"></a>
## `subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-message-ref"></a>
## `message/ref`

- Required: `yes`
- Shape: ref: `room-live-message.v2.schema.json#/properties/message~1ref`

<a id="field-message-seq-no"></a>
## `message/seq-no`

- Required: `yes`
- Shape: integer

<a id="field-content-type"></a>
## `content/type`

- Required: `yes`
- Shape: ref: `room-live-message.v2.schema.json#/properties/content~1type`

<a id="field-content-digest"></a>
## `content/digest`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/digest`

<a id="field-execution-provenance"></a>
## `execution/provenance`

- Required: `yes`
- Shape: ref: `inference-execution-provenance.v1.schema.json`
