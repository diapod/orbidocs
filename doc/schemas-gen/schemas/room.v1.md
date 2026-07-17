# Room v1

Source schema: [`doc/schemas/room.v1.schema.json`](../../schemas/room.v1.schema.json)

Durable room opening payload carried inside an Agora record envelope. The Agora envelope owns record id, topic, author and signature; this payload owns only room-domain fields.

## Governing Basis

- [`P070`](../../project/40-proposals/070-room-primitive.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`room/id`](#field-room-id) | `yes` | ref: `#/$defs/room_id` |  |
| [`opener/subject`](#field-opener-subject) | `yes` | ref: `#/$defs/subject` |  |
| [`authority/subject`](#field-authority-subject) | `yes` | ref: `#/$defs/subject` |  |
| [`policy/ref`](#field-policy-ref) | `yes` | string |  |
| [`seq/no`](#field-seq-no) | `yes` | integer |  |
| [`created-at`](#field-created-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `no` | string |  |
| [`source/ref`](#field-source-ref) | `no` | string |  |
| [`extensions`](#field-extensions) | `no` | ref: `#/$defs/extensions` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`room_id`](#def-room-id) | string |  |
| [`subject`](#def-subject) | object |  |
| [`grant`](#def-grant) | enum: `speak`, `vote`, `answer`, `observe`, `actuate`, `moderate`, `delegate` |  |
| [`extensions`](#def-extensions) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: ref: `#/$defs/room_id`

<a id="field-opener-subject"></a>
## `opener/subject`

- Required: `yes`
- Shape: ref: `#/$defs/subject`

<a id="field-authority-subject"></a>
## `authority/subject`

- Required: `yes`
- Shape: ref: `#/$defs/subject`

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `yes`
- Shape: string

<a id="field-seq-no"></a>
## `seq/no`

- Required: `yes`
- Shape: integer

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `no`
- Shape: string

<a id="field-source-ref"></a>
## `source/ref`

- Required: `no`
- Shape: string

<a id="field-extensions"></a>
## `extensions`

- Required: `no`
- Shape: ref: `#/$defs/extensions`

## Definition Semantics

<a id="def-room-id"></a>
## `$defs.room_id`

- Shape: string

<a id="def-subject"></a>
## `$defs.subject`

- Shape: object

<a id="def-grant"></a>
## `$defs.grant`

- Shape: enum: `speak`, `vote`, `answer`, `observe`, `actuate`, `moderate`, `delegate`

<a id="def-extensions"></a>
## `$defs.extensions`

- Shape: object
