# Whisper-adc-original-basis.local.v1

Source schema: [`doc/schemas/whisper-adc-original-basis.local.v1.schema.json`](../../schemas/whisper-adc-original-basis.local.v1.schema.json)

Private immutable registration binding to an already verified P035 original and its complete M_A set. No source inventory, custody hold, current count or release authorization is established by this descriptor. Never the public recipient proof.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-adc-original-basis.local.v1` |  |
| [`anchor/inputs`](#field-anchor-inputs) | `yes` | string |  |
| [`condition/original`](#field-condition-original) | `yes` | string |  |
| [`admission/evidence`](#field-admission-evidence) | `yes` | string |  |
| [`audience/manifests`](#field-audience-manifests) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-adc-original-basis.local.v1`

<a id="field-anchor-inputs"></a>
## `anchor/inputs`

- Required: `yes`
- Shape: string

<a id="field-condition-original"></a>
## `condition/original`

- Required: `yes`
- Shape: string

<a id="field-admission-evidence"></a>
## `admission/evidence`

- Required: `yes`
- Shape: string

<a id="field-audience-manifests"></a>
## `audience/manifests`

- Required: `yes`
- Shape: array
