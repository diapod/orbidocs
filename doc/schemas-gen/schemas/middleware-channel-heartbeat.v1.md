# Middleware Channel Heartbeat v1

Source schema: [`doc/schemas/middleware-channel-heartbeat.v1.schema.json`](../../schemas/middleware-channel-heartbeat.v1.schema.json)

Bounded application-level liveness signal for one channel session.

## Governing Basis

- [`doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`](../../project/40-proposals/080-multiplexed-middleware-channel-executor.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `middleware-channel-heartbeat.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`sent/at`](#field-sent-at) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `middleware-channel-heartbeat.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-sent-at"></a>
## `sent/at`

- Required: `yes`
- Shape: string
