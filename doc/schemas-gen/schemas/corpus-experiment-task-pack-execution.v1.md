# Corpus Experiment Task-pack Execution v1

Source schema: [`doc/schemas/corpus-experiment-task-pack-execution.v1.schema.json`](../../schemas/corpus-experiment-task-pack-execution.v1.schema.json)

Host-signed record, published to the Room, of one admitted task-pack experiment executed as a P094 run: the proposal, review and Chair decision it executes, the compiled plan and the run, the instance the run used, its concluded outcome, and bounded evidence artifacts each named by step and by the record's own instance. A later solver passage reads it as evidence; observations of one instance are never the current state of another. An observation run that does not pass the target verifier is recorded as `verification-failed`, an expected negative verdict; timeout, missing evidence and an isolation breach keep their own refusal codes. Every recorded run is concluded and names its result by digest; a refused run names its code, and an unknown outcome stays unknown: it is never consent to run the experiment again. The record carries refs and digests, never command output inline.

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
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`execution/ref`](#field-execution-ref) | `yes` | string |  |
| [`candidate/adoption-ref`](#field-candidate-adoption-ref) | `no` | ref: `corpus-task-pack-candidate-adoption.v1.schema.json#/properties/adoption~1ref` | The exact separate owner adoption, preserved by the handoff and covered by this execution signature. Required by the relation gate for a historical proposal. |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`proposal/ref`](#field-proposal-ref) | `yes` | string |  |
| [`proposal/digest`](#field-proposal-digest) | `yes` | string |  |
| [`review/ref`](#field-review-ref) | `yes` | string |  |
| [`review/digest`](#field-review-digest) | `yes` | string |  |
| [`decision/ref`](#field-decision-ref) | `yes` | string |  |
| [`decision/digest`](#field-decision-digest) | `yes` | string |  |
| [`candidate`](#field-candidate) | `yes` | unspecified |  |
| [`target`](#field-target) | `yes` | ref: `corpus-reasoning-experiment-proposal.v2.schema.json#/$defs/task-pack-target` |  |
| [`plan/ref`](#field-plan-ref) | `yes` | string |  |
| [`plan/digest`](#field-plan-digest) | `yes` | string |  |
| [`run/ref`](#field-run-ref) | `yes` | string |  |
| [`environment/ref`](#field-environment-ref) | `no` | string |  |
| [`outcome`](#field-outcome) | `yes` | enum: `verified`, `verification-failed`, `refused`, `cancelled`, `unknown` |  |
| [`refusal/code`](#field-refusal-code) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/refusalCode` |  |
| [`result/digest`](#field-result-digest) | `yes` | string |  |
| [`evidence`](#field-evidence) | `yes` | array |  |
| [`host/node-id`](#field-host-node-id) | `yes` | string |  |
| [`recorded-at`](#field-recorded-at) | `yes` | string |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `corpus-reasoning-experiment-proposal.v1.schema.json#/$defs/signature` |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "outcome": {
      "enum": [
        "refused"
      ]
    }
  },
  "required": [
    "outcome"
  ]
}
```

Then:

```json
{
  "required": [
    "refusal/code"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "outcome": {
      "enum": [
        "verified",
        "verification-failed"
      ]
    }
  },
  "required": [
    "outcome"
  ]
}
```

Then:

```json
{
  "required": [
    "environment/ref"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-execution-ref"></a>
## `execution/ref`

- Required: `yes`
- Shape: string

<a id="field-candidate-adoption-ref"></a>
## `candidate/adoption-ref`

- Required: `no`
- Shape: ref: `corpus-task-pack-candidate-adoption.v1.schema.json#/properties/adoption~1ref`

The exact separate owner adoption, preserved by the handoff and covered by this execution signature. Required by the relation gate for a historical proposal.

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: string

<a id="field-proposal-ref"></a>
## `proposal/ref`

- Required: `yes`
- Shape: string

<a id="field-proposal-digest"></a>
## `proposal/digest`

- Required: `yes`
- Shape: string

<a id="field-review-ref"></a>
## `review/ref`

- Required: `yes`
- Shape: string

<a id="field-review-digest"></a>
## `review/digest`

- Required: `yes`
- Shape: string

<a id="field-decision-ref"></a>
## `decision/ref`

- Required: `yes`
- Shape: string

<a id="field-decision-digest"></a>
## `decision/digest`

- Required: `yes`
- Shape: string

<a id="field-candidate"></a>
## `candidate`

- Required: `yes`
- Shape: unspecified

<a id="field-target"></a>
## `target`

- Required: `yes`
- Shape: ref: `corpus-reasoning-experiment-proposal.v2.schema.json#/$defs/task-pack-target`

<a id="field-plan-ref"></a>
## `plan/ref`

- Required: `yes`
- Shape: string

<a id="field-plan-digest"></a>
## `plan/digest`

- Required: `yes`
- Shape: string

<a id="field-run-ref"></a>
## `run/ref`

- Required: `yes`
- Shape: string

<a id="field-environment-ref"></a>
## `environment/ref`

- Required: `no`
- Shape: string

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: enum: `verified`, `verification-failed`, `refused`, `cancelled`, `unknown`

<a id="field-refusal-code"></a>
## `refusal/code`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/refusalCode`

<a id="field-result-digest"></a>
## `result/digest`

- Required: `yes`
- Shape: string

<a id="field-evidence"></a>
## `evidence`

- Required: `yes`
- Shape: array

<a id="field-host-node-id"></a>
## `host/node-id`

- Required: `yes`
- Shape: string

<a id="field-recorded-at"></a>
## `recorded-at`

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
