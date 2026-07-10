# Middleware Channel Hello v1

Source schema: [`doc/schemas/middleware-channel-hello.v1.schema.json`](../../schemas/middleware-channel-hello.v1.schema.json)

Module-supplied consistency assertions and requested limits for one authenticated channel launch.

## Governing Basis

- [`doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`](../../project/40-proposals/080-multiplexed-middleware-channel-executor.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `middleware-channel-hello.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`executor/id`](#field-executor-id) | `yes` | ref: `#/$defs/id` |  |
| [`module/id`](#field-module-id) | `yes` | ref: `#/$defs/id` |  |
| [`component/id`](#field-component-id) | `yes` | ref: `#/$defs/id` |  |
| [`launch/instance-id`](#field-launch-instance-id) | `yes` | ref: `#/$defs/id` |  |
| [`contract/versions`](#field-contract-versions) | `yes` | array |  |
| [`channel/features`](#field-channel-features) | `yes` | array |  |
| [`limits/requested`](#field-limits-requested) | `yes` | ref: `#/$defs/requestedLimits` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`id`](#def-id) | string |  |
| [`requestedLimits`](#def-requestedlimits) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `middleware-channel-hello.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-executor-id"></a>
## `executor/id`

- Required: `yes`
- Shape: ref: `#/$defs/id`

<a id="field-module-id"></a>
## `module/id`

- Required: `yes`
- Shape: ref: `#/$defs/id`

<a id="field-component-id"></a>
## `component/id`

- Required: `yes`
- Shape: ref: `#/$defs/id`

<a id="field-launch-instance-id"></a>
## `launch/instance-id`

- Required: `yes`
- Shape: ref: `#/$defs/id`

<a id="field-contract-versions"></a>
## `contract/versions`

- Required: `yes`
- Shape: array

<a id="field-channel-features"></a>
## `channel/features`

- Required: `yes`
- Shape: array

<a id="field-limits-requested"></a>
## `limits/requested`

- Required: `yes`
- Shape: ref: `#/$defs/requestedLimits`

## Definition Semantics

<a id="def-id"></a>
## `$defs.id`

- Shape: string

<a id="def-requestedlimits"></a>
## `$defs.requestedLimits`

- Shape: object
