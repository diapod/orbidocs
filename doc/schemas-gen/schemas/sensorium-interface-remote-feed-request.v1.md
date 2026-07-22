# Sensorium Interface Remote Feed Request v1

Source schema: [`doc/schemas/sensorium-interface-remote-feed-request.v1.schema.json`](../../schemas/sensorium-interface-remote-feed-request.v1.schema.json)

Starts one bounded owner-bound local projection of a remote Sensorium Interface subscription.

## Governing Basis

- [`doc/project/40-proposals/082-sensorium-interfaces.md`](../../project/40-proposals/082-sensorium-interfaces.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-remote-feed-request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`remote/node-id`](#field-remote-node-id) | `yes` | string |  |
| [`interface/id`](#field-interface-id) | `yes` | string |  |
| [`cursor/after`](#field-cursor-after) | `no` | string \| null |  |
| [`lease/requested-seconds`](#field-lease-requested-seconds) | `yes` | integer |  |
| [`batch`](#field-batch) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-remote-feed-request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-remote-node-id"></a>
## `remote/node-id`

- Required: `yes`
- Shape: string

<a id="field-interface-id"></a>
## `interface/id`

- Required: `yes`
- Shape: string

<a id="field-cursor-after"></a>
## `cursor/after`

- Required: `no`
- Shape: string | null

<a id="field-lease-requested-seconds"></a>
## `lease/requested-seconds`

- Required: `yes`
- Shape: integer

<a id="field-batch"></a>
## `batch`

- Required: `yes`
- Shape: object
