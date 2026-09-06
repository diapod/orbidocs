# Room Live Message v3

Source schema: [`doc/schemas/room-live-message.v3.schema.json`](../../schemas/room-live-message.v3.schema.json)

Explicit inference-aware successor; removing its immutable contribution evidence is invalid.

## Governing Basis

- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `3` |  |
| [`room/id`](#field-room-id) | `yes` | ref: `room-live-message.v2.schema.json#/properties/room~1id` |  |
| [`from/subject`](#field-from-subject) | `yes` | ref: `room-live-message.v2.schema.json#/properties/from~1subject` |  |
| [`seq/no`](#field-seq-no) | `yes` | ref: `room-live-message.v2.schema.json#/properties/seq~1no` |  |
| [`message/ref`](#field-message-ref) | `yes` | ref: `room-live-message.v2.schema.json#/properties/message~1ref` |  |
| [`reply/refs`](#field-reply-refs) | `no` | ref: `room-live-message.v2.schema.json#/properties/reply~1refs` |  |
| [`size/bytes`](#field-size-bytes) | `yes` | ref: `room-live-message.v2.schema.json#/properties/size~1bytes` |  |
| [`content/type`](#field-content-type) | `yes` | ref: `room-live-message.v2.schema.json#/properties/content~1type` |  |
| [`content`](#field-content) | `yes` | string |  |
| [`content/digest`](#field-content-digest) | `no` | ref: `room-live-message.v2.schema.json#/properties/content~1digest` |  |
| [`sent-at`](#field-sent-at) | `no` | ref: `room-live-message.v2.schema.json#/properties/sent-at` |  |
| [`extensions`](#field-extensions) | `yes` | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `3`

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: ref: `room-live-message.v2.schema.json#/properties/room~1id`

<a id="field-from-subject"></a>
## `from/subject`

- Required: `yes`
- Shape: ref: `room-live-message.v2.schema.json#/properties/from~1subject`

<a id="field-seq-no"></a>
## `seq/no`

- Required: `yes`
- Shape: ref: `room-live-message.v2.schema.json#/properties/seq~1no`

<a id="field-message-ref"></a>
## `message/ref`

- Required: `yes`
- Shape: ref: `room-live-message.v2.schema.json#/properties/message~1ref`

<a id="field-reply-refs"></a>
## `reply/refs`

- Required: `no`
- Shape: ref: `room-live-message.v2.schema.json#/properties/reply~1refs`

<a id="field-size-bytes"></a>
## `size/bytes`

- Required: `yes`
- Shape: ref: `room-live-message.v2.schema.json#/properties/size~1bytes`

<a id="field-content-type"></a>
## `content/type`

- Required: `yes`
- Shape: ref: `room-live-message.v2.schema.json#/properties/content~1type`

<a id="field-content"></a>
## `content`

- Required: `yes`
- Shape: string

<a id="field-content-digest"></a>
## `content/digest`

- Required: `no`
- Shape: ref: `room-live-message.v2.schema.json#/properties/content~1digest`

<a id="field-sent-at"></a>
## `sent-at`

- Required: `no`
- Shape: ref: `room-live-message.v2.schema.json#/properties/sent-at`

<a id="field-extensions"></a>
## `extensions`

- Required: `yes`
- Shape: object
