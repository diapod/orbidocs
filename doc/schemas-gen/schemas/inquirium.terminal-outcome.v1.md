# Inquirium Terminal Invocation Outcome

Source schema: [`doc/schemas/inquirium.terminal-outcome.v1.schema.json`](../../schemas/inquirium.terminal-outcome.v1.schema.json)

Sanitized terminal refusal or failure. Dispatch and egress are carried separately in exact result-bound provenance, not inferred from this outcome code.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inquirium.terminal-outcome.v1` |  |
| [`operation`](#field-operation) | `yes` | string |  |
| [`status`](#field-status) | `yes` | enum: `failed`, `refused` |  |
| [`reason/code`](#field-reason-code) | `yes` | enum: `runtime-execution-failed`, `result-publication-failed`, `result-retention-failed`, `retained-result-unavailable`, `invocation-refused` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.terminal-outcome.v1`

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: string

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `failed`, `refused`

<a id="field-reason-code"></a>
## `reason/code`

- Required: `yes`
- Shape: enum: `runtime-execution-failed`, `result-publication-failed`, `result-retention-failed`, `retained-result-unavailable`, `invocation-refused`
