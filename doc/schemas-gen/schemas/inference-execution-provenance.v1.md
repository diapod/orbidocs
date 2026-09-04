# Inference Execution Provenance v1

Source schema: [`doc/schemas/inference-execution-provenance.v1.schema.json`](../../schemas/inference-execution-provenance.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inference-execution-provenance.v1` |  |
| [`descriptor/digest`](#field-descriptor-digest) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/digest` |  |
| [`descriptor/size-bytes`](#field-descriptor-size-bytes) | `yes` | integer |  |
| [`descriptor`](#field-descriptor) | `no` | ref: `#/$defs/descriptor` |  |
| [`descriptor/ref`](#field-descriptor-ref) | `no` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
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
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/digest`

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
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

## Definition Semantics

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
