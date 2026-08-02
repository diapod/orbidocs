# Sensorium Web Source v1

Source schema: [`doc/schemas/sensorium-web-source.v1.schema.json`](../../schemas/sensorium-web-source.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-web-source.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`source/ref`](#field-source-ref) | `yes` | string |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | string |  |
| [`canonical/url`](#field-canonical-url) | `yes` | string |  |
| [`canonical/url-digest`](#field-canonical-url-digest) | `yes` | ref: `#/$defs/sha256Digest` |  |
| [`origin/policy-ref`](#field-origin-policy-ref) | `yes` | string |  |
| [`extraction/profile`](#field-extraction-profile) | `yes` | object |  |
| [`operational/context`](#field-operational-context) | `yes` | ref: `sensorium-operational-context.v1.schema.json` |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`sha256Digest`](#def-sha256digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-web-source.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-source-ref"></a>
## `source/ref`

- Required: `yes`
- Shape: string

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: string

<a id="field-canonical-url"></a>
## `canonical/url`

- Required: `yes`
- Shape: string

<a id="field-canonical-url-digest"></a>
## `canonical/url-digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256Digest`

<a id="field-origin-policy-ref"></a>
## `origin/policy-ref`

- Required: `yes`
- Shape: string

<a id="field-extraction-profile"></a>
## `extraction/profile`

- Required: `yes`
- Shape: object

<a id="field-operational-context"></a>
## `operational/context`

- Required: `yes`
- Shape: ref: `sensorium-operational-context.v1.schema.json`

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

## Definition Semantics

<a id="def-sha256digest"></a>
## `$defs.sha256Digest`

- Shape: string
