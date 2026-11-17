# Whisper-release-execution.v1

Source schema: [`doc/schemas/whisper-release-execution.v1.schema.json`](../../schemas/whisper-release-execution.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-release-execution.v1` |  |
| [`execution/nonce`](#field-execution-nonce) | `yes` | string |  |
| [`submission`](#field-submission) | `yes` | object |  |
| [`route`](#field-route) | `yes` | string |  |
| [`plan/digest`](#field-plan-digest) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-release-execution.v1`

<a id="field-execution-nonce"></a>
## `execution/nonce`

- Required: `yes`
- Shape: string

<a id="field-submission"></a>
## `submission`

- Required: `yes`
- Shape: object

<a id="field-route"></a>
## `route`

- Required: `yes`
- Shape: string

<a id="field-plan-digest"></a>
## `plan/digest`

- Required: `yes`
- Shape: string
