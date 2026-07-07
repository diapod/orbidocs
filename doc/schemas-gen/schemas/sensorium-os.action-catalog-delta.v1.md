# Sensorium-os.action-catalog-delta.v1

Source schema: [`doc/schemas/sensorium-os.action-catalog-delta.v1.schema.json`](../../schemas/sensorium-os.action-catalog-delta.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-os.action-catalog-delta.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`approval/ref`](#field-approval-ref) | `yes` | ref: `operator-consent-binding.v1.schema.json#/$defs/ref` |  |
| [`operator/ref`](#field-operator-ref) | `yes` | ref: `operator-consent-binding.v1.schema.json#/$defs/ref` |  |
| [`issued/at`](#field-issued-at) | `yes` | ref: `operator-consent-binding.v1.schema.json#/$defs/timestamp` |  |
| [`expires/at`](#field-expires-at) | `yes` | unspecified |  |
| [`revocation/ref`](#field-revocation-ref) | `yes` | unspecified |  |
| [`delta/digest`](#field-delta-digest) | `yes` | ref: `operator-consent-binding.v1.schema.json#/$defs/digest` |  |
| [`provenance`](#field-provenance) | `yes` | object |  |
| [`action`](#field-action) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-os.action-catalog-delta.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-approval-ref"></a>
## `approval/ref`

- Required: `yes`
- Shape: ref: `operator-consent-binding.v1.schema.json#/$defs/ref`

<a id="field-operator-ref"></a>
## `operator/ref`

- Required: `yes`
- Shape: ref: `operator-consent-binding.v1.schema.json#/$defs/ref`

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: ref: `operator-consent-binding.v1.schema.json#/$defs/timestamp`

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: unspecified

<a id="field-revocation-ref"></a>
## `revocation/ref`

- Required: `yes`
- Shape: unspecified

<a id="field-delta-digest"></a>
## `delta/digest`

- Required: `yes`
- Shape: ref: `operator-consent-binding.v1.schema.json#/$defs/digest`

<a id="field-provenance"></a>
## `provenance`

- Required: `yes`
- Shape: object

<a id="field-action"></a>
## `action`

- Required: `yes`
- Shape: object
