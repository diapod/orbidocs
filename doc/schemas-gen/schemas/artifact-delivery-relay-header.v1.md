# Artifact-delivery-relay-header.v1

Source schema: [`doc/schemas/artifact-delivery-relay-header.v1.schema.json`](../../schemas/artifact-delivery-relay-header.v1.schema.json)

JCS header of a binary bounded single-relay transport packet. Only forward names a configured circuit. Delivered carries no origin/route identity. Ciphertext is opaque and no sender domain authority is implied.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `artifact-delivery-relay-header.v1` |  |
| [`direction`](#field-direction) | `yes` | enum: `forward`, `return`, `delivered` |  |
| [`circuit/id`](#field-circuit-id) | `no` | string |  |
| [`return/handle`](#field-return-handle) | `yes` | string |  |
| [`family`](#field-family) | `yes` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`payload/size`](#field-payload-size) | `yes` | integer |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "direction": {
      "const": "forward"
    }
  }
}
```

Then:

```json
{
  "required": [
    "circuit/id"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `artifact-delivery-relay-header.v1`

<a id="field-direction"></a>
## `direction`

- Required: `yes`
- Shape: enum: `forward`, `return`, `delivered`

<a id="field-circuit-id"></a>
## `circuit/id`

- Required: `no`
- Shape: string

<a id="field-return-handle"></a>
## `return/handle`

- Required: `yes`
- Shape: string

<a id="field-family"></a>
## `family`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

<a id="field-payload-size"></a>
## `payload/size`

- Required: `yes`
- Shape: integer
