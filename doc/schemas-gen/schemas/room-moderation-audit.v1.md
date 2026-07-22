# Room Moderation Audit v1

Source schema: [`doc/schemas/room-moderation-audit.v1.schema.json`](../../schemas/room-moderation-audit.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/070-room-primitive.md`](../../project/40-proposals/070-room-primitive.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`audit/ref`](#field-audit-ref) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | ref: `room.v1.schema.json#/$defs/room_id` |  |
| [`action`](#field-action) | `yes` | enum: `invite`, `kick`, `remove`, `deny`, `reinstate`, `mute`, `unmute`, `floor-assign`, `floor-advance`, `floor-release` |  |
| [`decision`](#field-decision) | `yes` | enum: `admitted`, `refused`, `replayed`, `expired`, `cleanup-degraded` |  |
| [`actor/subject`](#field-actor-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`target/subject`](#field-target-subject) | `no` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`scope`](#field-scope) | `no` | enum: `membership/invite`, `membership/remove`, `membership/deny`, `grant/speak`, `moderation/delegate` |  |
| [`policy/generation`](#field-policy-generation) | `yes` | integer |  |
| [`room/seq-no`](#field-room-seq-no) | `yes` | integer |  |
| [`reason/code`](#field-reason-code) | `yes` | string |  |
| [`at`](#field-at) | `yes` | string |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-audit-ref"></a>
## `audit/ref`

- Required: `yes`
- Shape: string

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/room_id`

<a id="field-action"></a>
## `action`

- Required: `yes`
- Shape: enum: `invite`, `kick`, `remove`, `deny`, `reinstate`, `mute`, `unmute`, `floor-assign`, `floor-advance`, `floor-release`

<a id="field-decision"></a>
## `decision`

- Required: `yes`
- Shape: enum: `admitted`, `refused`, `replayed`, `expired`, `cleanup-degraded`

<a id="field-actor-subject"></a>
## `actor/subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-target-subject"></a>
## `target/subject`

- Required: `no`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-scope"></a>
## `scope`

- Required: `no`
- Shape: enum: `membership/invite`, `membership/remove`, `membership/deny`, `grant/speak`, `moderation/delegate`

<a id="field-policy-generation"></a>
## `policy/generation`

- Required: `yes`
- Shape: integer

<a id="field-room-seq-no"></a>
## `room/seq-no`

- Required: `yes`
- Shape: integer

<a id="field-reason-code"></a>
## `reason/code`

- Required: `yes`
- Shape: string

<a id="field-at"></a>
## `at`

- Required: `yes`
- Shape: string
