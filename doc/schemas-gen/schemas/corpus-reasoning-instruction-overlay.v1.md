# Corpus Reasoning Instruction Overlay v1

Source schema: [`doc/schemas/corpus-reasoning-instruction-overlay.v1.schema.json`](../../schemas/corpus-reasoning-instruction-overlay.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/064-inquirium-implementation-recommendations.md`](../../project/40-proposals/064-inquirium-implementation-recommendations.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)

### Stories

- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`overlay/id`](#field-overlay-id) | `yes` | string |  |
| [`assignment/id`](#field-assignment-id) | `yes` | string |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`participant`](#field-participant) | `yes` | ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject` |  |
| [`role`](#field-role) | `yes` | enum: `implementer`, `reviewer`, `adversarial-critic`, `summarizer` |  |
| [`turn/no`](#field-turn-no) | `yes` | integer |  |
| [`kind`](#field-kind) | `yes` | enum: `task-guidance`, `review-criteria`, `adversarial-check`, `summary-criteria` |  |
| [`position`](#field-position) | `yes` | enum: `preamble`, `postamble` |  |
| [`instruction/text`](#field-instruction-text) | `yes` | string |  |
| [`instruction/rendered`](#field-instruction-rendered) | `no` | string |  |
| [`class/key`](#field-class-key) | `yes` | enum: `Public`, `Community`, `Personal` |  |
| [`status`](#field-status) | `yes` | enum: `proposed`, `accepted`, `declined` |  |
| [`revision/no`](#field-revision-no) | `yes` | integer |  |
| [`proposed/by`](#field-proposed-by) | `yes` | string |  |
| [`proposed-at`](#field-proposed-at) | `yes` | string |  |
| [`decision/by`](#field-decision-by) | `no` | string |  |
| [`decided-at`](#field-decided-at) | `no` | string |  |
| [`policy/ref`](#field-policy-ref) | `no` | string |  |
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
          "policy/ref"
        ]
      },
      {
        "required": [
          "instruction/rendered"
        ]
      }
    ]
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "status": {
      "const": "accepted"
    }
  }
}
```

Then:

```json
{
  "required": [
    "instruction/rendered"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-overlay-id"></a>
## `overlay/id`

- Required: `yes`
- Shape: string

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

<a id="field-turn-no"></a>
## `turn/no`

- Required: `yes`
- Shape: integer

<a id="field-kind"></a>
## `kind`

- Required: `yes`
- Shape: enum: `task-guidance`, `review-criteria`, `adversarial-check`, `summary-criteria`

<a id="field-position"></a>
## `position`

- Required: `yes`
- Shape: enum: `preamble`, `postamble`

<a id="field-instruction-text"></a>
## `instruction/text`

- Required: `yes`
- Shape: string

<a id="field-instruction-rendered"></a>
## `instruction/rendered`

- Required: `no`
- Shape: string

<a id="field-class-key"></a>
## `class/key`

- Required: `yes`
- Shape: enum: `Public`, `Community`, `Personal`

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

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `no`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string
