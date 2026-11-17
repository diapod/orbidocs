# Whisper-adc-source-evaluation.local.v1

Source schema: [`doc/schemas/whisper-adc-source-evaluation.local.v1.schema.json`](../../schemas/whisper-adc-source-evaluation.local.v1.schema.json)

Private finite ADC candidate observation over an independently adopted complete local inventory. Not a portable count attestation, root, consent or source custody promise. Its raw membership/evidence identities must never enter a recipient package.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-adc-source-evaluation.local.v1` |  |
| [`anchor/inputs`](#field-anchor-inputs) | `yes` | string |  |
| [`condition/original`](#field-condition-original) | `yes` | string |  |
| [`request/digest`](#field-request-digest) | `yes` | string |  |
| [`source/pin`](#field-source-pin) | `yes` | object |  |
| [`epoch`](#field-epoch) | `yes` | integer |  |
| [`evidence/digest`](#field-evidence-digest) | `yes` | string |  |
| [`observed/at`](#field-observed-at) | `yes` | string |  |
| [`valid/until`](#field-valid-until) | `yes` | string |  |
| [`facts`](#field-facts) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-adc-source-evaluation.local.v1`

<a id="field-anchor-inputs"></a>
## `anchor/inputs`

- Required: `yes`
- Shape: string

<a id="field-condition-original"></a>
## `condition/original`

- Required: `yes`
- Shape: string

<a id="field-request-digest"></a>
## `request/digest`

- Required: `yes`
- Shape: string

<a id="field-source-pin"></a>
## `source/pin`

- Required: `yes`
- Shape: object

<a id="field-epoch"></a>
## `epoch`

- Required: `yes`
- Shape: integer

<a id="field-evidence-digest"></a>
## `evidence/digest`

- Required: `yes`
- Shape: string

<a id="field-observed-at"></a>
## `observed/at`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid/until`

- Required: `yes`
- Shape: string

<a id="field-facts"></a>
## `facts`

- Required: `yes`
- Shape: object
