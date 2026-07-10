# Middleware Channel Host Capability Call v1

Source schema: [`doc/schemas/middleware-channel-host-capability-call.v1.schema.json`](../../schemas/middleware-channel-host-capability-call.v1.schema.json)

Module-authored request body for invoking one host-authorized capability through an authenticated channel session.

## Governing Basis

- [`doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`](../../project/40-proposals/080-multiplexed-middleware-channel-executor.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `middleware-channel-host-capability-call.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`capability/id`](#field-capability-id) | `yes` | string |  |
| [`request/schema`](#field-request-schema) | `yes` | string |  |
| [`request`](#field-request) | `yes` | object |  |
| [`idempotency/key`](#field-idempotency-key) | `no` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `middleware-channel-host-capability-call.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-capability-id"></a>
## `capability/id`

- Required: `yes`
- Shape: string

<a id="field-request-schema"></a>
## `request/schema`

- Required: `yes`
- Shape: string

<a id="field-request"></a>
## `request`

- Required: `yes`
- Shape: object

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `no`
- Shape: string
