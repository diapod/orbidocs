# Corpus Task-pack Experiment Admission Response v1

Source schema: [`doc/schemas/corpus-task-pack-experiment.admit.response.v1.schema.json`](../../schemas/corpus-task-pack-experiment.admit.response.v1.schema.json)

The host's answer to a task-pack experiment admission: whether the chain was found again, and where its handoff stands. `running` names the run its engine drives; `published` carries the host-signed execution record; `refused` is a P094 refusal before the run, which recorded nothing; `needs-authorization`, `unauthorized` and `target-changed` stop before a new execution step; `stopped` is any other failure, after which the handoff resumes from its recorded facts.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-experiment.admit.response.v1` |  |
| [`replayed`](#field-replayed) | `yes` | boolean |  |
| [`proposal/ref`](#field-proposal-ref) | `yes` | string |  |
| [`handoff`](#field-handoff) | `yes` | ref: `#/$defs/handoff` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`handoff`](#def-handoff) | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-experiment.admit.response.v1`

<a id="field-replayed"></a>
## `replayed`

- Required: `yes`
- Shape: boolean

<a id="field-proposal-ref"></a>
## `proposal/ref`

- Required: `yes`
- Shape: string

<a id="field-handoff"></a>
## `handoff`

- Required: `yes`
- Shape: ref: `#/$defs/handoff`

## Definition Semantics

<a id="def-handoff"></a>
## `$defs.handoff`

- Shape: unspecified
