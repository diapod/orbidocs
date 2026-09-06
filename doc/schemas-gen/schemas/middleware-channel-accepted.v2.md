# Middleware Channel Accepted v2

Source schema: [`doc/schemas/middleware-channel-accepted.v2.schema.json`](../../schemas/middleware-channel-accepted.v2.schema.json)

Host-authenticated session identity, epoch, contract version, and effective limits.

## Governing Basis

- [`doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`](../../project/40-proposals/080-multiplexed-middleware-channel-executor.md)
- [`doc/project/40-proposals/086-component-communication-observation-and-trace-sessions.md`](../../project/40-proposals/086-component-communication-observation-and-trace-sessions.md)
- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `middleware-channel-accepted.v2` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `2` |  |
| [`session/id`](#field-session-id) | `yes` | ref: `middleware-channel-accepted.v1.schema.json#/properties/session~1id` |  |
| [`session/epoch`](#field-session-epoch) | `yes` | ref: `middleware-channel-accepted.v1.schema.json#/properties/session~1epoch` |  |
| [`contract/version`](#field-contract-version) | `yes` | const: `v2` |  |
| [`channel/features`](#field-channel-features) | `no` | ref: `middleware-channel-accepted.v1.schema.json#/properties/channel~1features` |  |
| [`limits/effective`](#field-limits-effective) | `yes` | ref: `middleware-channel-accepted.v1.schema.json#/properties/limits~1effective` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`effectiveLimits`](#def-effectivelimits) | ref: `middleware-channel-accepted.v1.schema.json#/$defs/effectiveLimits` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `middleware-channel-accepted.v2`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `2`

<a id="field-session-id"></a>
## `session/id`

- Required: `yes`
- Shape: ref: `middleware-channel-accepted.v1.schema.json#/properties/session~1id`

<a id="field-session-epoch"></a>
## `session/epoch`

- Required: `yes`
- Shape: ref: `middleware-channel-accepted.v1.schema.json#/properties/session~1epoch`

<a id="field-contract-version"></a>
## `contract/version`

- Required: `yes`
- Shape: const: `v2`

<a id="field-channel-features"></a>
## `channel/features`

- Required: `no`
- Shape: ref: `middleware-channel-accepted.v1.schema.json#/properties/channel~1features`

<a id="field-limits-effective"></a>
## `limits/effective`

- Required: `yes`
- Shape: ref: `middleware-channel-accepted.v1.schema.json#/properties/limits~1effective`

## Definition Semantics

<a id="def-effectivelimits"></a>
## `$defs.effectiveLimits`

- Shape: ref: `middleware-channel-accepted.v1.schema.json#/$defs/effectiveLimits`
