# Story-012-delegated-adaptive-executor-report.v1

Source schema: [`doc/schemas/story-012-delegated-adaptive-executor-report.v1.schema.json`](../../schemas/story-012-delegated-adaptive-executor-report.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `story-012-delegated-adaptive-executor-report.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`status`](#field-status) | `yes` | const: `partial` |  |
| [`profile/id`](#field-profile-id) | `yes` | const: `story-012-delegated-adaptive-executor` |  |
| [`evidence/boundary`](#field-evidence-boundary) | `yes` | const: `derived-from-retained-single-host-full-system` |  |
| [`source/report`](#field-source-report) | `yes` | string |  |
| [`source/report/sha256`](#field-source-report-sha256) | `yes` | string |  |
| [`requester/node`](#field-requester-node) | `yes` | const: `node-a` |  |
| [`executor/designation`](#field-executor-designation) | `yes` | object | Names the remote participant Agent that produced the candidate. This is a delegation designation, never direct Sensorium effect authority; node A retains admission and P083 execution authority. |
| [`experiment/count`](#field-experiment-count) | `yes` | const: `2` |  |
| [`p083/lifecycle`](#field-p083-lifecycle) | `yes` | array |  |
| [`room-prose/direct-effect-count`](#field-room-prose-direct-effect-count) | `yes` | const: `0` |  |
| [`proven/invariants`](#field-proven-invariants) | `yes` | array |  |
| [`unproven/invariants`](#field-unproven-invariants) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `story-012-delegated-adaptive-executor-report.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: const: `partial`

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

Names the remote participant Agent that produced the candidate. This is a delegation designation, never direct Sensorium effect authority; node A retains admission and P083 execution authority.

<a id="field-experiment-count"></a>
## `experiment/count`

- Required: `yes`
- Shape: const: `2`

<a id="field-p083-lifecycle"></a>
## `p083/lifecycle`

- Required: `yes`
- Shape: array

<a id="field-room-prose-direct-effect-count"></a>
## `room-prose/direct-effect-count`

- Required: `yes`
- Shape: const: `0`

<a id="field-proven-invariants"></a>
## `proven/invariants`

- Required: `yes`
- Shape: array

<a id="field-unproven-invariants"></a>
## `unproven/invariants`

- Required: `yes`
- Shape: array
