# Corpus Reasoning Experiment Proposal v2

Source schema: [`doc/schemas/corpus-reasoning-experiment-proposal.v2.schema.json`](../../schemas/corpus-reasoning-experiment-proposal.v2.schema.json)

Signed portable envelope binding one content-addressed inert candidate artifact of a named type to the exact query, Room, retained turn, author node, requester-selected executor, classification, expiry and HIL requirement. Unlike v1, which promises an `inquirium.candidate-plan.v1`, v2 names the artifact type, so the executor is selected by type. A P094 task-pack candidate (`operator-task-experiment-candidate.v1`) also names its target, the exact task profile and local binding, and can only be executed by the `deterministic-host-compiler` mode. The envelope carries no effect authority: package activation, a current operator binding and HIL remain required at execution.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)
- [`doc/project/30-stories/story-013-qmail-task-pack.md`](../../project/30-stories/story-013-qmail-task-pack.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-013-qmail-task-pack.md`](../../project/30-stories/story-013-qmail-task-pack.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `2` |  |
| [`proposal/ref`](#field-proposal-ref) | `yes` | string |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`turn/id`](#field-turn-id) | `yes` | string |  |
| [`author`](#field-author) | `yes` | ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject` |  |
| [`author/node-id`](#field-author-node-id) | `yes` | string |  |
| [`executor`](#field-executor) | `yes` | ref: `corpus-reasoning-experiment-proposal.v1.schema.json#/$defs/executor` |  |
| [`candidate`](#field-candidate) | `yes` | ref: `#/$defs/candidate` |  |
| [`target`](#field-target) | `no` | ref: `#/$defs/task-pack-target` |  |
| [`class/key`](#field-class-key) | `yes` | enum: `Public`, `Community`, `Personal` |  |
| [`human-in-loop/required`](#field-human-in-loop-required) | `yes` | const: `True` |  |
| [`proposed-at`](#field-proposed-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `corpus-reasoning-experiment-proposal.v1.schema.json#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`candidate`](#def-candidate) | object | One content-addressed candidate artifact of a named type. The artifact ref is the object-store address of the digest. |
| [`task-pack-target`](#def-task-pack-target) | object | The P094 task profile and local binding a task-pack candidate is meant for. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "candidate": {
      "properties": {
        "artifact/type": {
          "const": "operator-task-experiment-candidate.v1"
        }
      },
      "required": [
        "artifact/type"
      ]
    }
  },
  "required": [
    "candidate"
  ]
}
```

Then:

```json
{
  "required": [
    "target"
  ],
  "properties": {
    "executor": {
      "properties": {
        "mode": {
          "const": "deterministic-host-compiler"
        }
      }
    }
  }
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `2`

<a id="field-proposal-ref"></a>
## `proposal/ref`

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

<a id="field-turn-id"></a>
## `turn/id`

- Required: `yes`
- Shape: string

<a id="field-author"></a>
## `author`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject`

<a id="field-author-node-id"></a>
## `author/node-id`

- Required: `yes`
- Shape: string

<a id="field-executor"></a>
## `executor`

- Required: `yes`
- Shape: ref: `corpus-reasoning-experiment-proposal.v1.schema.json#/$defs/executor`

<a id="field-candidate"></a>
## `candidate`

- Required: `yes`
- Shape: ref: `#/$defs/candidate`

<a id="field-target"></a>
## `target`

- Required: `no`
- Shape: ref: `#/$defs/task-pack-target`

<a id="field-class-key"></a>
## `class/key`

- Required: `yes`
- Shape: enum: `Public`, `Community`, `Personal`

<a id="field-human-in-loop-required"></a>
## `human-in-loop/required`

- Required: `yes`
- Shape: const: `True`

<a id="field-proposed-at"></a>
## `proposed-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `corpus-reasoning-experiment-proposal.v1.schema.json#/$defs/signature`

## Definition Semantics

<a id="def-candidate"></a>
## `$defs.candidate`

- Shape: object

One content-addressed candidate artifact of a named type. The artifact ref is the object-store address of the digest.

<a id="def-task-pack-target"></a>
## `$defs.task-pack-target`

- Shape: object

The P094 task profile and local binding a task-pack candidate is meant for.
