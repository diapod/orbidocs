# Sensorium Interface Actuation Descriptor v1

Source schema: [`doc/schemas/sensorium-interface-actuation-descriptor.v1.schema.json`](../../schemas/sensorium-interface-actuation-descriptor.v1.schema.json)

Immutable publication contract for one effect-bearing Sensorium Interface.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-actuation-descriptor.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`interface/id`](#field-interface-id) | `yes` | ref: `#/$defs/interface_ref` |  |
| [`interface/kind`](#field-interface-kind) | `yes` | const: `actuation` |  |
| [`interface/name`](#field-interface-name) | `yes` | string |  |
| [`publisher/node-ref`](#field-publisher-node-ref) | `yes` | string |  |
| [`methods`](#field-methods) | `yes` | array |  |
| [`receipt/schema-ref`](#field-receipt-schema-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`coordination/mode`](#field-coordination-mode) | `yes` | enum: `shared`, `exclusive-lease` |  |
| [`classification/max-tier`](#field-classification-max-tier) | `yes` | enum: `Public`, `Community`, `Personal` |  |
| [`classification/topic-class`](#field-classification-topic-class) | `yes` | string |  |
| [`redaction/profile-ref`](#field-redaction-profile-ref) | `no` | ref: `#/$defs/ref` |  |
| [`limits`](#field-limits) | `yes` | ref: `#/$defs/limits` |  |
| [`published/at`](#field-published-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`interface_ref`](#def-interface-ref) | string |  |
| [`limits`](#def-limits) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "coordination/mode": {
      "const": "exclusive-lease"
    }
  },
  "required": [
    "coordination/mode"
  ]
}
```

Then:

```json
{
  "properties": {
    "limits": {
      "required": [
        "claim/queue-max",
        "claim/wait-max-ms",
        "lease/quantum-max-ms",
        "lease/cumulative-max-ms"
      ]
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-actuation-descriptor.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-interface-id"></a>
## `interface/id`

- Required: `yes`
- Shape: ref: `#/$defs/interface_ref`

<a id="field-interface-kind"></a>
## `interface/kind`

- Required: `yes`
- Shape: const: `actuation`

<a id="field-interface-name"></a>
## `interface/name`

- Required: `yes`
- Shape: string

<a id="field-publisher-node-ref"></a>
## `publisher/node-ref`

- Required: `yes`
- Shape: string

<a id="field-methods"></a>
## `methods`

- Required: `yes`
- Shape: array

<a id="field-receipt-schema-ref"></a>
## `receipt/schema-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-coordination-mode"></a>
## `coordination/mode`

- Required: `yes`
- Shape: enum: `shared`, `exclusive-lease`

<a id="field-classification-max-tier"></a>
## `classification/max-tier`

- Required: `yes`
- Shape: enum: `Public`, `Community`, `Personal`

<a id="field-classification-topic-class"></a>
## `classification/topic-class`

- Required: `yes`
- Shape: string

<a id="field-redaction-profile-ref"></a>
## `redaction/profile-ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-limits"></a>
## `limits`

- Required: `yes`
- Shape: ref: `#/$defs/limits`

<a id="field-published-at"></a>
## `published/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-interface-ref"></a>
## `$defs.interface_ref`

- Shape: string

<a id="def-limits"></a>
## `$defs.limits`

- Shape: object
