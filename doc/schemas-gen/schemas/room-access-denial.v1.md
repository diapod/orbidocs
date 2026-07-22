# Room Access Denial v1

Source schema: [`doc/schemas/room-access-denial.v1.schema.json`](../../schemas/room-access-denial.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/070-room-primitive.md`](../../project/40-proposals/070-room-primitive.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`room/id`](#field-room-id) | `yes` | ref: `room.v1.schema.json#/$defs/room_id` |  |
| [`denial/ref`](#field-denial-ref) | `yes` | string |  |
| [`op`](#field-op) | `yes` | enum: `deny`, `reinstate` |  |
| [`subject`](#field-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`authority/subject`](#field-authority-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`seq/no`](#field-seq-no) | `yes` | integer |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `no` | string |  |
| [`supersedes/ref`](#field-supersedes-ref) | `no` | string |  |
| [`reason/code`](#field-reason-code) | `yes` | string |  |
| [`reason/ref`](#field-reason-ref) | `no` | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "op": {
      "const": "deny"
    }
  },
  "required": [
    "op"
  ]
}
```

Then:

```json
{
  "not": {
    "required": [
      "supersedes/ref"
    ]
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "op": {
      "const": "reinstate"
    }
  },
  "required": [
    "op"
  ]
}
```

Then:

```json
{
  "required": [
    "supersedes/ref"
  ],
  "not": {
    "required": [
      "expires-at"
    ]
  }
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/room_id`

<a id="field-denial-ref"></a>
## `denial/ref`

- Required: `yes`
- Shape: string

<a id="field-op"></a>
## `op`

- Required: `yes`
- Shape: enum: `deny`, `reinstate`

<a id="field-subject"></a>
## `subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

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

<a id="field-expires-at"></a>
## `expires-at`

- Required: `no`
- Shape: string

<a id="field-supersedes-ref"></a>
## `supersedes/ref`

- Required: `no`
- Shape: string

<a id="field-reason-code"></a>
## `reason/code`

- Required: `yes`
- Shape: string

<a id="field-reason-ref"></a>
## `reason/ref`

- Required: `no`
- Shape: string
