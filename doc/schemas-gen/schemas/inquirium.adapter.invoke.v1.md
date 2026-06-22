# Inquirium Adapter Invoke v1

Source schema: [`doc/schemas/inquirium.adapter.invoke.v1.schema.json`](../../schemas/inquirium.adapter.invoke.v1.schema.json)

Neutral text-generation invocation payload accepted by middleware-hosted Inquirium adapters.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inquirium.adapter.invoke.v1` |  |
| [`operation`](#field-operation) | `yes` | enum: `text.generate`, `text.respond`, `chat.completion` |  |
| [`model`](#field-model) | `yes` | string |  |
| [`input`](#field-input) | `yes` | object |  |
| [`parameters`](#field-parameters) | `no` | object |  |
| [`metadata`](#field-metadata) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`message`](#def-message) | object |  |
| [`textBlock`](#def-textblock) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.adapter.invoke.v1`

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: enum: `text.generate`, `text.respond`, `chat.completion`

<a id="field-model"></a>
## `model`

- Required: `yes`
- Shape: string

<a id="field-input"></a>
## `input`

- Required: `yes`
- Shape: object

<a id="field-parameters"></a>
## `parameters`

- Required: `no`
- Shape: object

<a id="field-metadata"></a>
## `metadata`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-message"></a>
## `$defs.message`

- Shape: object

<a id="def-textblock"></a>
## `$defs.textBlock`

- Shape: object
