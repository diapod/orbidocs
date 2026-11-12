# Whisper-reviewed-publication-result.local.v1

Source schema: [`doc/schemas/whisper-reviewed-publication-result.local.v1.schema.json`](../../schemas/whisper-reviewed-publication-result.local.v1.schema.json)

Fresh check of an existing exact locally reviewed signed artifact. Contains no custody token, claim references or private horizons.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`record/id`](#field-record-id) | `yes` | string |  |
| [`schema`](#field-schema) | `yes` | const: `whisper-reviewed-publication-result.local.v1` |  |
| [`checked`](#field-checked) | `yes` | const: `True` |  |
## Field Semantics

<a id="field-record-id"></a>
## `record/id`

- Required: `yes`
- Shape: string

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-reviewed-publication-result.local.v1`

<a id="field-checked"></a>
## `checked`

- Required: `yes`
- Shape: const: `True`
