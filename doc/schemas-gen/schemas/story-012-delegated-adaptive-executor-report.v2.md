# Story-012-delegated-adaptive-executor-report.v2

Source schema: [`doc/schemas/story-012-delegated-adaptive-executor-report.v2.schema.json`](../../schemas/story-012-delegated-adaptive-executor-report.v2.schema.json)

Closed evidence that a remote participant Agent authored an inert CandidatePlan while requester node A retained HIL and P083 effect authority.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `story-012-delegated-adaptive-executor-report.v2` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `2` |  |
| [`status`](#field-status) | `yes` | const: `passed` |  |
| [`profile/id`](#field-profile-id) | `yes` | const: `story-012-delegated-adaptive-executor` |  |
| [`evidence/boundary`](#field-evidence-boundary) | `yes` | const: `derived-from-retained-single-host-full-system` |  |
| [`source/report`](#field-source-report) | `yes` | string |  |
| [`source/report/sha256`](#field-source-report-sha256) | `yes` | string |  |
| [`requester/node`](#field-requester-node) | `yes` | const: `node-a` |  |
| [`executor/designation`](#field-executor-designation) | `yes` | object |  |
| [`experiment/count`](#field-experiment-count) | `yes` | const: `2` |  |
| [`p083/lifecycle`](#field-p083-lifecycle) | `yes` | const: `['claim', 'invoke', 'release']` |  |
| [`room-prose/direct-effect-count`](#field-room-prose-direct-effect-count) | `yes` | const: `0` |  |
| [`evidence/experiments`](#field-evidence-experiments) | `yes` | array |  |
| [`proven/invariants`](#field-proven-invariants) | `yes` | array |  |
| [`unproven/invariants`](#field-unproven-invariants) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`invariant`](#def-invariant) | enum: `candidate-plan-is-attributed-and-inert`, `failed-plan-observation-precedes-correction`, `fresh-lease-per-effect`, `operator-question-precedes-effect`, `p083-claim-invoke-release-only`, `requester-retains-effect-authority`, `room-prose-has-no-direct-effect` |  |
| [`experiment-evidence`](#def-experiment-evidence) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `story-012-delegated-adaptive-executor-report.v2`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `2`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: const: `passed`

<a id="field-profile-id"></a>
## `profile/id`

- Required: `yes`
- Shape: const: `story-012-delegated-adaptive-executor`

<a id="field-evidence-boundary"></a>
## `evidence/boundary`

- Required: `yes`
- Shape: const: `derived-from-retained-single-host-full-system`

<a id="field-source-report"></a>
## `source/report`

- Required: `yes`
- Shape: string

<a id="field-source-report-sha256"></a>
## `source/report/sha256`

- Required: `yes`
- Shape: string

<a id="field-requester-node"></a>
## `requester/node`

- Required: `yes`
- Shape: const: `node-a`

<a id="field-executor-designation"></a>
## `executor/designation`

- Required: `yes`
- Shape: object

<a id="field-experiment-count"></a>
## `experiment/count`

- Required: `yes`
- Shape: const: `2`

<a id="field-p083-lifecycle"></a>
## `p083/lifecycle`

- Required: `yes`
- Shape: const: `['claim', 'invoke', 'release']`

<a id="field-room-prose-direct-effect-count"></a>
## `room-prose/direct-effect-count`

- Required: `yes`
- Shape: const: `0`

<a id="field-evidence-experiments"></a>
## `evidence/experiments`

- Required: `yes`
- Shape: array

<a id="field-proven-invariants"></a>
## `proven/invariants`

- Required: `yes`
- Shape: array

<a id="field-unproven-invariants"></a>
## `unproven/invariants`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-invariant"></a>
## `$defs.invariant`

- Shape: enum: `candidate-plan-is-attributed-and-inert`, `failed-plan-observation-precedes-correction`, `fresh-lease-per-effect`, `operator-question-precedes-effect`, `p083-claim-invoke-release-only`, `requester-retains-effect-authority`, `room-prose-has-no-direct-effect`

<a id="def-experiment-evidence"></a>
## `$defs.experiment-evidence`

- Shape: object
