# Whisper-authoring-output-policy.local.v1

Source schema: [`doc/schemas/whisper-authoring-output-policy.local.v1.schema.json`](../../schemas/whisper-authoring-output-policy.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/authoring-output-retention.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/authoring-output-retention.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`retry/seconds`](#field-retry-seconds) | `yes` | integer |  |
| [`custody`](#field-custody) | `yes` | enum: `disabled`, `enabled` |  |
## Field Semantics

<a id="field-retry-seconds"></a>
## `retry/seconds`

- Required: `yes`
- Shape: integer

<a id="field-custody"></a>
## `custody`

- Required: `yes`
- Shape: enum: `disabled`, `enabled`
