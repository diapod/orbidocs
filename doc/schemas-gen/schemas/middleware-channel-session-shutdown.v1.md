# Middleware Channel Session Shutdown v1

Source schema: [`doc/schemas/middleware-channel-session-shutdown.v1.schema.json`](../../schemas/middleware-channel-session-shutdown.v1.schema.json)

Host-issued bounded drain deadline and redacted reason for one channel session shutdown.

## Governing Basis

- [`doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`](../../project/40-proposals/080-multiplexed-middleware-channel-executor.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `middleware-channel-session-shutdown.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`deadline/at`](#field-deadline-at) | `yes` | string |  |
| [`reason`](#field-reason) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `middleware-channel-session-shutdown.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-deadline-at"></a>
## `deadline/at`

- Required: `yes`
- Shape: string

<a id="field-reason"></a>
## `reason`

- Required: `yes`
- Shape: string
