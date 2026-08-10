# Sensorium Web Extraction Result v1

Source schema: [`doc/schemas/sensorium-web-extraction-result.v1.schema.json`](../../schemas/sensorium-web-extraction-result.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-web-extraction-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`outcome`](#field-outcome) | `yes` | enum: `completed`, `low-confidence`, `empty`, `refused`, `failed` |  |
| [`source/ref`](#field-source-ref) | `yes` | string |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | string |  |
| [`fetch/result-digest`](#field-fetch-result-digest) | `yes` | ref: `#/$defs/sha256Digest` |  |
| [`extraction/profile-ref`](#field-extraction-profile-ref) | `yes` | const: `sensorium-web-extraction:static-stdlib-main-v1` |  |
| [`extraction/profile-digest`](#field-extraction-profile-digest) | `yes` | const: `sha256:lW1Oos_09Srd_Vrze9X8ZwPK-W0Hjpsjl9ss9PYqbAg` |  |
| [`representation/digest`](#field-representation-digest) | `no` | ref: `#/$defs/sha256Digest` |  |
| [`representation`](#field-representation) | `no` | ref: `sensorium-web-document-blocks.v1.schema.json` |  |
| [`confidence/basis`](#field-confidence-basis) | `no` | enum: `sufficient-text`, `short-text` |  |
| [`failure`](#field-failure) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`sha256Digest`](#def-sha256digest) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "outcome": {
      "enum": [
        "completed",
        "low-confidence"
      ]
    }
  },
  "required": [
    "outcome"
  ]
}
```

Then:

```json
{
  "required": [
    "representation/digest",
    "representation",
    "confidence/basis"
  ],
  "not": {
    "required": [
      "failure"
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-web-extraction-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: enum: `completed`, `low-confidence`, `empty`, `refused`, `failed`

<a id="field-source-ref"></a>
## `source/ref`

- Required: `yes`
- Shape: string

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: string

<a id="field-fetch-result-digest"></a>
## `fetch/result-digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256Digest`

<a id="field-extraction-profile-ref"></a>
## `extraction/profile-ref`

- Required: `yes`
- Shape: const: `sensorium-web-extraction:static-stdlib-main-v1`

<a id="field-extraction-profile-digest"></a>
## `extraction/profile-digest`

- Required: `yes`
- Shape: const: `sha256:lW1Oos_09Srd_Vrze9X8ZwPK-W0Hjpsjl9ss9PYqbAg`

<a id="field-representation-digest"></a>
## `representation/digest`

- Required: `no`
- Shape: ref: `#/$defs/sha256Digest`

<a id="field-representation"></a>
## `representation`

- Required: `no`
- Shape: ref: `sensorium-web-document-blocks.v1.schema.json`

<a id="field-confidence-basis"></a>
## `confidence/basis`

- Required: `no`
- Shape: enum: `sufficient-text`, `short-text`

<a id="field-failure"></a>
## `failure`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-sha256digest"></a>
## `$defs.sha256Digest`

- Shape: string
