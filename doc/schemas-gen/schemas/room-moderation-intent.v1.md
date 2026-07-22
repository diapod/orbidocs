# Room Moderation Intent v1

Source schema: [`doc/schemas/room-moderation-intent.v1.schema.json`](../../schemas/room-moderation-intent.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/070-room-primitive.md`](../../project/40-proposals/070-room-primitive.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`intent/ref`](#field-intent-ref) | `yes` | string |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | ref: `room.v1.schema.json#/$defs/room_id` |  |
| [`action`](#field-action) | `yes` | enum: `invite`, `kick`, `remove`, `deny`, `reinstate`, `mute`, `unmute`, `floor-assign`, `floor-advance`, `floor-release` |  |
| [`target/subject`](#field-target-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`expected/high-water`](#field-expected-high-water) | `yes` | integer |  |
| [`policy/generation`](#field-policy-generation) | `yes` | integer |  |
| [`expires-at`](#field-expires-at) | `no` | string |  |
| [`supersedes/ref`](#field-supersedes-ref) | `no` | string |  |
| [`reason/code`](#field-reason-code) | `yes` | string |  |
| [`reason/ref`](#field-reason-ref) | `no` | string |  |
| [`requested-at`](#field-requested-at) | `yes` | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "action": {
      "const": "deny"
    }
  },
  "required": [
    "action"
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
    "action": {
      "const": "reinstate"
    }
  },
  "required": [
    "action"
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

### Rule 3

When:

```json
{
  "properties": {
    "action": {
      "not": {
        "enum": [
          "deny",
          "reinstate"
        ]
      }
    }
  },
  "required": [
    "action"
  ]
}
```

Then:

```json
{
  "not": {
    "anyOf": [
      {
        "required": [
          "expires-at"
        ]
      },
      {
        "required": [
          "supersedes/ref"
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

<a id="field-intent-ref"></a>
## `intent/ref`

- Required: `yes`
- Shape: string

<a id="field-idempotency-key"></a>
## `idempotency/key`

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

<a id="field-target-subject"></a>
## `target/subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-expected-high-water"></a>
## `expected/high-water`

- Required: `yes`
- Shape: integer

<a id="field-policy-generation"></a>
## `policy/generation`

- Required: `yes`
- Shape: integer

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

<a id="field-requested-at"></a>
## `requested-at`

- Required: `yes`
- Shape: string
