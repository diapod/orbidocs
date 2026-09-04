# Inference Execution Posture v1

Source schema: [`doc/schemas/inference-execution-posture.v1.schema.json`](../../schemas/inference-execution-posture.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inference-execution-posture.v1` |  |
| [`posture/id`](#field-posture-id) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/digest` |  |
| [`assertion/owner`](#field-assertion-owner) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`subject/ref`](#field-subject-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`scope/ref`](#field-scope-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`generation`](#field-generation) | `yes` | integer |  |
| [`processing-boundary/ref`](#field-processing-boundary-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`locality`](#field-locality) | `yes` | enum: `local-only`, `may-use-non-local`, `non-local-required`, `unknown` |  |
| [`provider/disclosure`](#field-provider-disclosure) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/provider-disclosure` |  |
| [`provider/refs`](#field-provider-refs) | `yes` | array |  |
| [`valid/from`](#field-valid-from) | `yes` | string |  |
| [`valid/until`](#field-valid-until) | `no` | string |  |
| [`evidence/requirements`](#field-evidence-requirements) | `yes` | array |  |
| [`extensions`](#field-extensions) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/extensions` |  |

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
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/digest`

<a id="field-assertion-owner"></a>
## `assertion/owner`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-subject-ref"></a>
## `subject/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-scope-ref"></a>
## `scope/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-generation"></a>
## `generation`

- Required: `yes`
- Shape: integer

<a id="field-processing-boundary-ref"></a>
## `processing-boundary/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-locality"></a>
## `locality`

- Required: `yes`
- Shape: enum: `local-only`, `may-use-non-local`, `non-local-required`, `unknown`

<a id="field-provider-disclosure"></a>
## `provider/disclosure`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/provider-disclosure`

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
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/extensions`
