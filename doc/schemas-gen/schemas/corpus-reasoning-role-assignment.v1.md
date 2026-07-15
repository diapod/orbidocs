# Corpus Reasoning Role Assignment v1

Source schema: [`doc/schemas/corpus-reasoning-role-assignment.v1.schema.json`](../../schemas/corpus-reasoning-role-assignment.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`assignment/id`](#field-assignment-id) | `yes` | string |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`participant`](#field-participant) | `yes` | ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject` |  |
| [`role`](#field-role) | `yes` | enum: `implementer`, `reviewer`, `adversarial-critic`, `summarizer` |  |
| [`status`](#field-status) | `yes` | enum: `proposed`, `accepted`, `declined` |  |
| [`revision/no`](#field-revision-no) | `yes` | integer |  |
| [`proposed/by`](#field-proposed-by) | `yes` | string |  |
| [`proposed-at`](#field-proposed-at) | `yes` | string |  |
| [`decision/by`](#field-decision-by) | `no` | string |  |
| [`decided-at`](#field-decided-at) | `no` | string |  |
| [`acceptance/mode`](#field-acceptance-mode) | `no` | enum: `local-participant`, `local-policy` |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "status": {
      "const": "proposed"
    }
  }
}
```

Then:

```json
{
  "not": {
    "anyOf": [
      {
        "required": [
          "decision/by"
        ]
      },
      {
        "required": [
          "decided-at"
        ]
      },
      {
        "required": [
          "acceptance/mode"
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

<a id="field-assignment-id"></a>
## `assignment/id`

- Required: `yes`
- Shape: string

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: string

<a id="field-participant"></a>
## `participant`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject`

<a id="field-role"></a>
## `role`

- Required: `yes`
- Shape: enum: `implementer`, `reviewer`, `adversarial-critic`, `summarizer`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `proposed`, `accepted`, `declined`

<a id="field-revision-no"></a>
## `revision/no`

- Required: `yes`
- Shape: integer

<a id="field-proposed-by"></a>
## `proposed/by`

- Required: `yes`
- Shape: string

<a id="field-proposed-at"></a>
## `proposed-at`

- Required: `yes`
- Shape: string

<a id="field-decision-by"></a>
## `decision/by`

- Required: `no`
- Shape: string

<a id="field-decided-at"></a>
## `decided-at`

- Required: `no`
- Shape: string

<a id="field-acceptance-mode"></a>
## `acceptance/mode`

- Required: `no`
- Shape: enum: `local-participant`, `local-policy`

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string
