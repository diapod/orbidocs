# Room Event v1

Source schema: [`doc/schemas/room-event.v1.schema.json`](../../schemas/room-event.v1.schema.json)

Durable room lifecycle or scoped authority event payload carried by an Agora record envelope.

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
| [`delegation/id`](#field-delegation-id) | `no` | string |  |
| [`delegation/scopes`](#field-delegation-scopes) | `no` | array |  |
| [`delegation/expires-at`](#field-delegation-expires-at) | `no` | string |  |
| [`delegation/ref`](#field-delegation-ref) | `no` | string |  |
| [`seq/no`](#field-seq-no) | `yes` | integer |  |
| [`created-at`](#field-created-at) | `yes` | string |  |
| [`reason/ref`](#field-reason-ref) | `no` | string |  |
| [`extensions`](#field-extensions) | `no` | ref: `room.v1.schema.json#/$defs/extensions` |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "event": {
      "const": "delegated"
    }
  },
  "required": [
    "event"
  ]
}
```

Then:

```json
{
  "required": [
    "subject",
    "delegation/id",
    "delegation/scopes",
    "delegation/expires-at"
  ],
  "not": {
    "required": [
      "delegation/ref"
    ]
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "event": {
      "const": "delegation-revoked"
    }
  },
  "required": [
    "event"
  ]
}
```

Then:

```json
{
  "required": [
    "delegation/ref"
  ],
  "not": {
    "anyOf": [
      {
        "required": [
          "delegation/id"
        ]
      },
      {
        "required": [
          "delegation/scopes"
        ]
      },
      {
        "required": [
          "delegation/expires-at"
        ]
      }
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

<a id="field-delegation-id"></a>
## `delegation/id`

- Required: `no`
- Shape: string

<a id="field-delegation-scopes"></a>
## `delegation/scopes`

- Required: `no`
- Shape: array

<a id="field-delegation-expires-at"></a>
## `delegation/expires-at`

- Required: `no`
- Shape: string

<a id="field-delegation-ref"></a>
## `delegation/ref`

- Required: `no`
- Shape: string

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
