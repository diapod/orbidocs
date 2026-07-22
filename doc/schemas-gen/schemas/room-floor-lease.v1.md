# Room Floor Lease v1

Source schema: [`doc/schemas/room-floor-lease.v1.schema.json`](../../schemas/room-floor-lease.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/070-room-primitive.md`](../../project/40-proposals/070-room-primitive.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`lease/ref`](#field-lease-ref) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | ref: `room.v1.schema.json#/$defs/room_id` |  |
| [`subject`](#field-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`issuer/subject`](#field-issuer-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`policy/generation`](#field-policy-generation) | `yes` | integer |  |
| [`issuance/seq-no`](#field-issuance-seq-no) | `yes` | integer |  |
| [`renewal/no`](#field-renewal-no) | `yes` | integer |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-lease-ref"></a>
## `lease/ref`

- Required: `yes`
- Shape: string

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/room_id`

<a id="field-subject"></a>
## `subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-issuer-subject"></a>
## `issuer/subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-policy-generation"></a>
## `policy/generation`

- Required: `yes`
- Shape: integer

<a id="field-issuance-seq-no"></a>
## `issuance/seq-no`

- Required: `yes`
- Shape: integer

<a id="field-renewal-no"></a>
## `renewal/no`

- Required: `yes`
- Shape: integer

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string
