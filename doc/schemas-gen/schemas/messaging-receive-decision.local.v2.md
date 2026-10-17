# Messaging Current Receive Authority Decision v2

Source schema: [`doc/schemas/messaging-receive-decision.local.v2.schema.json`](../../schemas/messaging-receive-decision.local.v2.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `messaging-receive-decision.local.v2` |  |
| [`authorized`](#field-authorized) | `yes` | boolean |  |
| [`basis`](#field-basis) | `yes` | unspecified |  |
| [`reasons`](#field-reasons) | `yes` | array |  |
| [`observed_at`](#field-observed-at) | `yes` | string |  |
| [`evidence`](#field-evidence) | `yes` | object |  |
| [`authority/failure`](#field-authority-failure) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "authorized": {
      "const": true
    }
  }
}
```

Then:

```json
{
  "properties": {
    "basis": {
      "type": "object"
    },
    "reasons": {
      "maxItems": 0
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `messaging-receive-decision.local.v2`

<a id="field-authorized"></a>
## `authorized`

- Required: `yes`
- Shape: boolean

<a id="field-basis"></a>
## `basis`

- Required: `yes`
- Shape: unspecified

<a id="field-reasons"></a>
## `reasons`

- Required: `yes`
- Shape: array

<a id="field-observed-at"></a>
## `observed_at`

- Required: `yes`
- Shape: string

<a id="field-evidence"></a>
## `evidence`

- Required: `yes`
- Shape: object

<a id="field-authority-failure"></a>
## `authority/failure`

- Required: `no`
- Shape: object
