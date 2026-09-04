# Inference Execution Provenance v1

Source schema: [`doc/schemas/inference-execution-provenance.v1.schema.json`](../../schemas/inference-execution-provenance.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inference-execution-provenance.v1` |  |
| [`descriptor/digest`](#field-descriptor-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`descriptor/size-bytes`](#field-descriptor-size-bytes) | `yes` | integer |  |
| [`descriptor`](#field-descriptor) | `no` | ref: `#/$defs/descriptor` |  |
| [`descriptor/ref`](#field-descriptor-ref) | `no` | ref: `#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`provider-ref`](#def-provider-ref) | string |  |
| [`provider-disclosure`](#def-provider-disclosure) | enum: `complete`, `partial`, `withheld`, `unknown` |  |
| [`evidence-basis`](#def-evidence-basis) | unspecified |  |
| [`extensions`](#def-extensions) | object |  |
| [`bindings`](#def-bindings) | object |  |
| [`evidence`](#def-evidence) | object |  |
| [`lineage`](#def-lineage) | object |  |
| [`descriptor`](#def-descriptor) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "descriptor"
  ]
}
```

Then:

```json
{
  "properties": {
    "descriptor/size-bytes": {
      "maximum": 16384
    }
  }
}
```

### Rule 2

When:

```json
{
  "required": [
    "descriptor/ref"
  ]
}
```

Then:

```json
{
  "properties": {
    "descriptor/size-bytes": {
      "minimum": 16385
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inference-execution-provenance.v1`

<a id="field-descriptor-digest"></a>
## `descriptor/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-descriptor-size-bytes"></a>
## `descriptor/size-bytes`

- Required: `yes`
- Shape: integer

<a id="field-descriptor"></a>
## `descriptor`

- Required: `no`
- Shape: ref: `#/$defs/descriptor`

<a id="field-descriptor-ref"></a>
## `descriptor/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

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

<a id="def-bindings"></a>
## `$defs.bindings`

- Shape: object

<a id="def-evidence"></a>
## `$defs.evidence`

- Shape: object

<a id="def-lineage"></a>
## `$defs.lineage`

- Shape: object

<a id="def-descriptor"></a>
## `$defs.descriptor`

- Shape: object
