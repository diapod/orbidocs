# Middleware Channel Accepted v1

Source schema: [`doc/schemas/middleware-channel-accepted.v1.schema.json`](../../schemas/middleware-channel-accepted.v1.schema.json)

Host-authenticated session identity, epoch, contract version, and effective limits.

## Governing Basis

- [`doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`](../../project/40-proposals/080-multiplexed-middleware-channel-executor.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `middleware-channel-accepted.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`session/id`](#field-session-id) | `yes` | string |  |
| [`session/epoch`](#field-session-epoch) | `yes` | integer |  |
| [`contract/version`](#field-contract-version) | `yes` | const: `v1` |  |
| [`limits/effective`](#field-limits-effective) | `yes` | ref: `#/$defs/effectiveLimits` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`effectiveLimits`](#def-effectivelimits) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `middleware-channel-accepted.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-session-id"></a>
## `session/id`

- Required: `yes`
- Shape: string

<a id="field-session-epoch"></a>
## `session/epoch`

- Required: `yes`
- Shape: integer

<a id="field-contract-version"></a>
## `contract/version`

- Required: `yes`
- Shape: const: `v1`

<a id="field-limits-effective"></a>
## `limits/effective`

- Required: `yes`
- Shape: ref: `#/$defs/effectiveLimits`

## Definition Semantics

<a id="def-effectivelimits"></a>
## `$defs.effectiveLimits`

- Shape: object
