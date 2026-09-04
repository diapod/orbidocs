# Inference Execution Posture v1

Source schema: [`doc/schemas/inference-execution-posture.v1.schema.json`](../../schemas/inference-execution-posture.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inference-execution-posture.v1` |  |
| [`posture/id`](#field-posture-id) | `yes` | ref: `#/$defs/digest` |  |
| [`assertion/owner`](#field-assertion-owner) | `yes` | ref: `#/$defs/ref` |  |
| [`subject/ref`](#field-subject-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`scope/ref`](#field-scope-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`generation`](#field-generation) | `yes` | integer |  |
| [`processing-boundary/ref`](#field-processing-boundary-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`locality`](#field-locality) | `yes` | enum: `local-only`, `may-use-non-local`, `non-local-required`, `unknown` |  |
| [`provider/disclosure`](#field-provider-disclosure) | `yes` | ref: `#/$defs/provider-disclosure` |  |
| [`provider/refs`](#field-provider-refs) | `yes` | array |  |
| [`valid/from`](#field-valid-from) | `yes` | string |  |
| [`valid/until`](#field-valid-until) | `no` | string |  |
| [`evidence/requirements`](#field-evidence-requirements) | `yes` | array |  |
| [`extensions`](#field-extensions) | `yes` | ref: `#/$defs/extensions` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`provider-ref`](#def-provider-ref) | string |  |
| [`provider-disclosure`](#def-provider-disclosure) | enum: `complete`, `partial`, `withheld`, `unknown` |  |
| [`evidence-basis`](#def-evidence-basis) | unspecified |  |
| [`extensions`](#def-extensions) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "provider/disclosure"
  ],
  "properties": {
    "provider/disclosure": {
      "const": "partial"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "provider/refs": {
      "minItems": 1
    }
  }
}
```

### Rule 2

When:

```json
{
  "required": [
    "provider/disclosure"
  ],
  "properties": {
    "provider/disclosure": {
      "enum": [
        "withheld",
        "unknown"
      ]
    }
  }
}
```

Then:

```json
{
  "properties": {
    "provider/refs": {
      "maxItems": 0
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inference-execution-posture.v1`

<a id="field-posture-id"></a>
## `posture/id`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-assertion-owner"></a>
## `assertion/owner`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-subject-ref"></a>
## `subject/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-scope-ref"></a>
## `scope/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-generation"></a>
## `generation`

- Required: `yes`
- Shape: integer

<a id="field-processing-boundary-ref"></a>
## `processing-boundary/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-locality"></a>
## `locality`

- Required: `yes`
- Shape: enum: `local-only`, `may-use-non-local`, `non-local-required`, `unknown`

<a id="field-provider-disclosure"></a>
## `provider/disclosure`

- Required: `yes`
- Shape: ref: `#/$defs/provider-disclosure`

<a id="field-provider-refs"></a>
## `provider/refs`

- Required: `yes`
- Shape: array

<a id="field-valid-from"></a>
## `valid/from`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid/until`

- Required: `no`
- Shape: string

<a id="field-evidence-requirements"></a>
## `evidence/requirements`

- Required: `yes`
- Shape: array

<a id="field-extensions"></a>
## `extensions`

- Required: `yes`
- Shape: ref: `#/$defs/extensions`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-provider-ref"></a>
## `$defs.provider-ref`

- Shape: string

<a id="def-provider-disclosure"></a>
## `$defs.provider-disclosure`

- Shape: enum: `complete`, `partial`, `withheld`, `unknown`

<a id="def-evidence-basis"></a>
## `$defs.evidence-basis`

- Shape: unspecified

<a id="def-extensions"></a>
## `$defs.extensions`

- Shape: object
