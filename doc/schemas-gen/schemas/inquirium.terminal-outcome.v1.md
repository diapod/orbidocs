# Inquirium Failed Invocation

Source schema: [`doc/schemas/inquirium.terminal-outcome.v1.schema.json`](../../schemas/inquirium.terminal-outcome.v1.schema.json)

Sanitized terminal failure. Dispatch and egress are carried separately in exact result-bound provenance, not inferred from this failure code.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inquirium.terminal-outcome.v1` |  |
| [`operation`](#field-operation) | `yes` | string |  |
| [`status`](#field-status) | `yes` | const: `failed` |  |
| [`reason/code`](#field-reason-code) | `yes` | enum: `runtime-execution-failed`, `result-publication-failed` |  |
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
- Shape: const: `failed`

<a id="field-reason-code"></a>
## `reason/code`

- Required: `yes`
- Shape: enum: `runtime-execution-failed`, `result-publication-failed`
