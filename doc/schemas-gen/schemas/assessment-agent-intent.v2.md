# Assessment-agent-intent.v2

Source schema: [`doc/schemas/assessment-agent-intent.v2.schema.json`](../../schemas/assessment-agent-intent.v2.schema.json)

P026-012b-r1 successor. Historical versions are unchanged; private commitments have explicit HMAC labels.

## Governing Basis

- [`doc/project/40-proposals/026-assessment-agent-consumer-r1.md`](../../project/40-proposals/026-assessment-agent-consumer-r1.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `assessment-agent-intent.v2` |  |
| [`agent/ref`](#field-agent-ref) | `yes` | string |  |
| [`binding/ref`](#field-binding-ref) | `yes` | string |  |
| [`consumer-policy/ref`](#field-consumer-policy-ref) | `yes` | string |  |
| [`source/approval-ref`](#field-source-approval-ref) | `yes` | string |  |
| [`source/intent-digest`](#field-source-intent-digest) | `yes` | string |  |
| [`source/activation-ref`](#field-source-activation-ref) | `yes` | string |  |
| [`launch/alias`](#field-launch-alias) | `yes` | string |  |
| [`daemon/boot`](#field-daemon-boot) | `yes` | string |  |
| [`executor/ref`](#field-executor-ref) | `yes` | string |  |
| [`module/ref`](#field-module-ref) | `yes` | string |  |
| [`component/ref`](#field-component-ref) | `yes` | string |  |
| [`participant/ref`](#field-participant-ref) | `yes` | string |  |
| [`operator/binding`](#field-operator-binding) | `yes` | string |  |
| [`subject`](#field-subject) | `yes` | object |  |
| [`runtime/ref`](#field-runtime-ref) | `yes` | string \| null |  |
| [`task/ref`](#field-task-ref) | `yes` | const: `assessment-agent-review:v1` |  |
| [`time/deadline-utc`](#field-time-deadline-utc) | `yes` | string |  |
| [`budget`](#field-budget) | `yes` | object |  |
| [`memory`](#field-memory) | `yes` | const: `none` |  |
| [`fork`](#field-fork) | `yes` | const: `deny` |  |
| [`output/sink`](#field-output-sink) | `yes` | const: `module-private-result` |  |
| [`result/max-bytes`](#field-result-max-bytes) | `yes` | const: `262144` |  |
| [`cost/mode`](#field-cost-mode) | `yes` | const: `unmetered` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `assessment-agent-intent.v2`

<a id="field-agent-ref"></a>
## `agent/ref`

- Required: `yes`
- Shape: string

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: string

<a id="field-consumer-policy-ref"></a>
## `consumer-policy/ref`

- Required: `yes`
- Shape: string

<a id="field-source-approval-ref"></a>
## `source/approval-ref`

- Required: `yes`
- Shape: string

<a id="field-source-intent-digest"></a>
## `source/intent-digest`

- Required: `yes`
- Shape: string

<a id="field-source-activation-ref"></a>
## `source/activation-ref`

- Required: `yes`
- Shape: string

<a id="field-launch-alias"></a>
## `launch/alias`

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

<a id="field-participant-ref"></a>
## `participant/ref`

- Required: `yes`
- Shape: string

<a id="field-operator-binding"></a>
## `operator/binding`

- Required: `yes`
- Shape: string

<a id="field-subject"></a>
## `subject`

- Required: `yes`
- Shape: object

<a id="field-runtime-ref"></a>
## `runtime/ref`

- Required: `yes`
- Shape: string | null

<a id="field-task-ref"></a>
## `task/ref`

- Required: `yes`
- Shape: const: `assessment-agent-review:v1`

<a id="field-time-deadline-utc"></a>
## `time/deadline-utc`

- Required: `yes`
- Shape: string

<a id="field-budget"></a>
## `budget`

- Required: `yes`
- Shape: object

<a id="field-memory"></a>
## `memory`

- Required: `yes`
- Shape: const: `none`

<a id="field-fork"></a>
## `fork`

- Required: `yes`
- Shape: const: `deny`

<a id="field-output-sink"></a>
## `output/sink`

- Required: `yes`
- Shape: const: `module-private-result`

<a id="field-result-max-bytes"></a>
## `result/max-bytes`

- Required: `yes`
- Shape: const: `262144`

<a id="field-cost-mode"></a>
## `cost/mode`

- Required: `yes`
- Shape: const: `unmetered`
