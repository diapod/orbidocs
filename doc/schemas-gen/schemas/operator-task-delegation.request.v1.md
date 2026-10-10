# Operator-task-delegation.request.v1

Source schema: [`doc/schemas/operator-task-delegation.request.v1.schema.json`](../../schemas/operator-task-delegation.request.v1.schema.json)

Local control choices or approval of a retained preview. No private key, passphrase, replacement document or widened authority is accepted.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-delegation.request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`action`](#field-action) | `yes` | enum: `prepare`, `commit`, `revoke`, `status`, `prepare-plan`, `approve-run`, `start-turn`, `admit-reviewed`, `admit-experiment` |  |
| [`query/id`](#field-query-id) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/operatorBindingRef` |  |
| [`allowed/actions`](#field-allowed-actions) | `no` | array |  |
| [`agent/profile-refs`](#field-agent-profile-refs) | `no` | array |  |
| [`valid/until`](#field-valid-until) | `no` | string |  |
| [`preview/ref`](#field-preview-ref) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`approved/digest`](#field-approved-digest) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`run/ref`](#field-run-ref) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`choices`](#field-choices) | `no` | ref: `corpus-task-pack-turn.prepare.request.v1.schema.json` |  |
| [`review/ref`](#field-review-ref) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`proposal/ref`](#field-proposal-ref) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`decision/ref`](#field-decision-ref) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-delegation.request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-action"></a>
## `action`

- Required: `yes`
- Shape: enum: `prepare`, `commit`, `revoke`, `status`, `prepare-plan`, `approve-run`, `start-turn`, `admit-reviewed`, `admit-experiment`

<a id="field-query-id"></a>
## `query/id`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/operatorBindingRef`

<a id="field-allowed-actions"></a>
## `allowed/actions`

- Required: `no`
- Shape: array

<a id="field-agent-profile-refs"></a>
## `agent/profile-refs`

- Required: `no`
- Shape: array

<a id="field-valid-until"></a>
## `valid/until`

- Required: `no`
- Shape: string

<a id="field-preview-ref"></a>
## `preview/ref`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-approved-digest"></a>
## `approved/digest`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-run-ref"></a>
## `run/ref`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-choices"></a>
## `choices`

- Required: `no`
- Shape: ref: `corpus-task-pack-turn.prepare.request.v1.schema.json`

<a id="field-review-ref"></a>
## `review/ref`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-proposal-ref"></a>
## `proposal/ref`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-decision-ref"></a>
## `decision/ref`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`
