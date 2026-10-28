# Assessment-viewer-intent.v1

Source schema: [`doc/schemas/assessment-viewer-intent.v1.schema.json`](../../schemas/assessment-viewer-intent.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/026-assessment-viewer-grants.md`](../../project/40-proposals/026-assessment-viewer-grants.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`node/ref`](#field-node-ref) | `yes` | string |  |
| [`daemon/boot`](#field-daemon-boot) | `yes` | string |  |
| [`executor/ref`](#field-executor-ref) | `yes` | string |  |
| [`module/ref`](#field-module-ref) | `yes` | string |  |
| [`component/ref`](#field-component-ref) | `yes` | string |  |
| [`launch/ref`](#field-launch-ref) | `yes` | string |  |
| [`launch/alias`](#field-launch-alias) | `yes` | string |  |
| [`participant/ref`](#field-participant-ref) | `yes` | string |  |
| [`operator/binding`](#field-operator-binding) | `yes` | string |  |
| [`schema`](#field-schema) | `yes` | const: `assessment-viewer-intent.v1` |  |
| [`purpose`](#field-purpose) | `yes` | const: `assessment-view` |  |
| [`operation`](#field-operation) | `yes` | const: `agora.assessment.read` |  |
| [`subjects`](#field-subjects) | `yes` | array |  |
| [`time/proposal-utc`](#field-time-proposal-utc) | `yes` | string |  |
| [`time/deadline-utc`](#field-time-deadline-utc) | `yes` | string |  |
| [`time/proposal-mono-ms`](#field-time-proposal-mono-ms) | `yes` | integer |  |
| [`time/deadline-mono-ms`](#field-time-deadline-mono-ms) | `yes` | integer |  |
| [`ttl/seconds`](#field-ttl-seconds) | `yes` | integer |  |
| [`budget/attempts`](#field-budget-attempts) | `yes` | const: `30` |  |
| [`budget/window-seconds`](#field-budget-window-seconds) | `yes` | const: `60` |  |
| [`budget/in-flight`](#field-budget-in-flight) | `yes` | const: `1` |  |
| [`activation/ref`](#field-activation-ref) | `yes` | string |  |
## Field Semantics

<a id="field-node-ref"></a>
## `node/ref`

- Required: `yes`
- Shape: string

<a id="field-daemon-boot"></a>
## `daemon/boot`

- Required: `yes`
- Shape: string

<a id="field-executor-ref"></a>
## `executor/ref`

- Required: `yes`
- Shape: string

<a id="field-module-ref"></a>
## `module/ref`

- Required: `yes`
- Shape: string

<a id="field-component-ref"></a>
## `component/ref`

- Required: `yes`
- Shape: string

<a id="field-launch-ref"></a>
## `launch/ref`

- Required: `yes`
- Shape: string

<a id="field-launch-alias"></a>
## `launch/alias`

- Required: `yes`
- Shape: string

<a id="field-participant-ref"></a>
## `participant/ref`

- Required: `yes`
- Shape: string

<a id="field-operator-binding"></a>
## `operator/binding`

- Required: `yes`
- Shape: string

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `assessment-viewer-intent.v1`

<a id="field-purpose"></a>
## `purpose`

- Required: `yes`
- Shape: const: `assessment-view`

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: const: `agora.assessment.read`

<a id="field-subjects"></a>
## `subjects`

- Required: `yes`
- Shape: array

<a id="field-time-proposal-utc"></a>
## `time/proposal-utc`

- Required: `yes`
- Shape: string

<a id="field-time-deadline-utc"></a>
## `time/deadline-utc`

- Required: `yes`
- Shape: string

<a id="field-time-proposal-mono-ms"></a>
## `time/proposal-mono-ms`

- Required: `yes`
- Shape: integer

<a id="field-time-deadline-mono-ms"></a>
## `time/deadline-mono-ms`

- Required: `yes`
- Shape: integer

<a id="field-ttl-seconds"></a>
## `ttl/seconds`

- Required: `yes`
- Shape: integer

<a id="field-budget-attempts"></a>
## `budget/attempts`

- Required: `yes`
- Shape: const: `30`

<a id="field-budget-window-seconds"></a>
## `budget/window-seconds`

- Required: `yes`
- Shape: const: `60`

<a id="field-budget-in-flight"></a>
## `budget/in-flight`

- Required: `yes`
- Shape: const: `1`

<a id="field-activation-ref"></a>
## `activation/ref`

- Required: `yes`
- Shape: string
