# Room Floor Policy v1

Source schema: [`doc/schemas/room-floor-policy.v1.schema.json`](../../schemas/room-floor-policy.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/070-room-primitive.md`](../../project/40-proposals/070-room-primitive.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`room/id`](#field-room-id) | `yes` | ref: `room.v1.schema.json#/$defs/room_id` |  |
| [`policy/ref`](#field-policy-ref) | `yes` | string |  |
| [`mode`](#field-mode) | `yes` | enum: `open`, `moderated`, `round-robin` |  |
| [`generation`](#field-generation) | `yes` | integer |  |
| [`queue/max`](#field-queue-max) | `yes` | integer |  |
| [`lease/ttl-seconds`](#field-lease-ttl-seconds) | `yes` | integer |  |
| [`lease/renewal-max`](#field-lease-renewal-max) | `yes` | integer |  |
| [`lease/outstanding-max`](#field-lease-outstanding-max) | `yes` | integer |  |
| [`authority/subject`](#field-authority-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`seq/no`](#field-seq-no) | `yes` | integer |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/room_id`

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `yes`
- Shape: string

<a id="field-mode"></a>
## `mode`

- Required: `yes`
- Shape: enum: `open`, `moderated`, `round-robin`

<a id="field-generation"></a>
## `generation`

- Required: `yes`
- Shape: integer

<a id="field-queue-max"></a>
## `queue/max`

- Required: `yes`
- Shape: integer

<a id="field-lease-ttl-seconds"></a>
## `lease/ttl-seconds`

- Required: `yes`
- Shape: integer

<a id="field-lease-renewal-max"></a>
## `lease/renewal-max`

- Required: `yes`
- Shape: integer

<a id="field-lease-outstanding-max"></a>
## `lease/outstanding-max`

- Required: `yes`
- Shape: integer

<a id="field-authority-subject"></a>
## `authority/subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-seq-no"></a>
## `seq/no`

- Required: `yes`
- Shape: integer

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string
