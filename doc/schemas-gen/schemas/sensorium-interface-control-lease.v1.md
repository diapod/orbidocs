# Sensorium Interface Control Lease v1

Source schema: [`doc/schemas/sensorium-interface-control-lease.v1.schema.json`](../../schemas/sensorium-interface-control-lease.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-control-lease.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`interface/id`](#field-interface-id) | `yes` | ref: `#/$defs/interface_ref` |  |
| [`holder/ref`](#field-holder-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`grant/id`](#field-grant-id) | `yes` | ref: `#/$defs/ref` |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`lease/id`](#field-lease-id) | `yes` | string |  |
| [`lease/epoch`](#field-lease-epoch) | `yes` | integer |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`hold/cumulative-ms`](#field-hold-cumulative-ms) | `yes` | integer |  |
| [`methods`](#field-methods) | `yes` | array |  |
| [`limits`](#field-limits) | `yes` | ref: `sensorium-interface-actuation-grant-scope.v1.schema.json#/$defs/limits` |  |
| [`authority/refs`](#field-authority-refs) | `yes` | array |  |
| [`caller/last-sequence`](#field-caller-last-sequence) | `no` | integer |  |
| [`operator/held`](#field-operator-held) | `no` | boolean |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`interface_ref`](#def-interface-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-control-lease.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-interface-id"></a>
## `interface/id`

- Required: `yes`
- Shape: ref: `#/$defs/interface_ref`

<a id="field-holder-ref"></a>
## `holder/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-grant-id"></a>
## `grant/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-lease-id"></a>
## `lease/id`

- Required: `yes`
- Shape: string

<a id="field-lease-epoch"></a>
## `lease/epoch`

- Required: `yes`
- Shape: integer

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

<a id="field-hold-cumulative-ms"></a>
## `hold/cumulative-ms`

- Required: `yes`
- Shape: integer

<a id="field-methods"></a>
## `methods`

- Required: `yes`
- Shape: array

<a id="field-limits"></a>
## `limits`

- Required: `yes`
- Shape: ref: `sensorium-interface-actuation-grant-scope.v1.schema.json#/$defs/limits`

<a id="field-authority-refs"></a>
## `authority/refs`

- Required: `yes`
- Shape: array

<a id="field-caller-last-sequence"></a>
## `caller/last-sequence`

- Required: `no`
- Shape: integer

<a id="field-operator-held"></a>
## `operator/held`

- Required: `no`
- Shape: boolean

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-interface-ref"></a>
## `$defs.interface_ref`

- Shape: string
