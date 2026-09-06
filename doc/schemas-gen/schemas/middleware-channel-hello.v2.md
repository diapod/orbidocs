# Middleware Channel Hello v2

Source schema: [`doc/schemas/middleware-channel-hello.v2.schema.json`](../../schemas/middleware-channel-hello.v2.schema.json)

Module-supplied consistency assertions and requested limits for one authenticated channel launch.

## Governing Basis

- [`doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`](../../project/40-proposals/080-multiplexed-middleware-channel-executor.md)
- [`doc/project/40-proposals/086-component-communication-observation-and-trace-sessions.md`](../../project/40-proposals/086-component-communication-observation-and-trace-sessions.md)
- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `middleware-channel-hello.v2` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `2` |  |
| [`executor/id`](#field-executor-id) | `yes` | ref: `middleware-channel-hello.v1.schema.json#/properties/executor~1id` |  |
| [`module/id`](#field-module-id) | `yes` | ref: `middleware-channel-hello.v1.schema.json#/properties/module~1id` |  |
| [`component/id`](#field-component-id) | `yes` | ref: `middleware-channel-hello.v1.schema.json#/properties/component~1id` |  |
| [`launch/instance-id`](#field-launch-instance-id) | `yes` | ref: `middleware-channel-hello.v1.schema.json#/properties/launch~1instance-id` |  |
| [`channel/features`](#field-channel-features) | `yes` | ref: `middleware-channel-hello.v1.schema.json#/properties/channel~1features` |  |
| [`limits/requested`](#field-limits-requested) | `yes` | ref: `middleware-channel-hello.v1.schema.json#/properties/limits~1requested` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`id`](#def-id) | ref: `middleware-channel-hello.v1.schema.json#/$defs/id` |  |
| [`requestedLimits`](#def-requestedlimits) | ref: `middleware-channel-hello.v1.schema.json#/$defs/requestedLimits` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `middleware-channel-hello.v2`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `2`

<a id="field-executor-id"></a>
## `executor/id`

- Required: `yes`
- Shape: ref: `middleware-channel-hello.v1.schema.json#/properties/executor~1id`

<a id="field-module-id"></a>
## `module/id`

- Required: `yes`
- Shape: ref: `middleware-channel-hello.v1.schema.json#/properties/module~1id`

<a id="field-component-id"></a>
## `component/id`

- Required: `yes`
- Shape: ref: `middleware-channel-hello.v1.schema.json#/properties/component~1id`

<a id="field-launch-instance-id"></a>
## `launch/instance-id`

- Required: `yes`
- Shape: ref: `middleware-channel-hello.v1.schema.json#/properties/launch~1instance-id`

<a id="field-channel-features"></a>
## `channel/features`

- Required: `yes`
- Shape: ref: `middleware-channel-hello.v1.schema.json#/properties/channel~1features`

<a id="field-limits-requested"></a>
## `limits/requested`

- Required: `yes`
- Shape: ref: `middleware-channel-hello.v1.schema.json#/properties/limits~1requested`

## Definition Semantics

<a id="def-id"></a>
## `$defs.id`

- Shape: ref: `middleware-channel-hello.v1.schema.json#/$defs/id`

<a id="def-requestedlimits"></a>
## `$defs.requestedLimits`

- Shape: ref: `middleware-channel-hello.v1.schema.json#/$defs/requestedLimits`
