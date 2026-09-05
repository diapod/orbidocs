# Inference Consumption Policy v1

Source schema: [`doc/schemas/inference-consumption-policy.v1.schema.json`](../../schemas/inference-consumption-policy.v1.schema.json)

Receiving owner's explicit policy, independent of a producer declaration or execution evidence. Missing evidence is unknown; policy evaluation never rewrites producer evidence or grants authority.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inference-consumption-policy.v1` |  |
| [`processing-boundary/ref`](#field-processing-boundary-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`locality`](#field-locality) | `yes` | enum: `local-only`, `may-use-non-local`, `non-local-required`, `unknown` |  |
| [`provider/allow`](#field-provider-allow) | `yes` | array |  |
| [`provider/deny`](#field-provider-deny) | `yes` | array |  |
| [`unknown/policy`](#field-unknown-policy) | `yes` | enum: `deny`, `warn`, `allow` |  |
| [`evidence/complete-required`](#field-evidence-complete-required) | `yes` | boolean |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inference-consumption-policy.v1`

<a id="field-processing-boundary-ref"></a>
## `processing-boundary/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-locality"></a>
## `locality`

- Required: `yes`
- Shape: enum: `local-only`, `may-use-non-local`, `non-local-required`, `unknown`

<a id="field-provider-allow"></a>
## `provider/allow`

- Required: `yes`
- Shape: array

<a id="field-provider-deny"></a>
## `provider/deny`

- Required: `yes`
- Shape: array

<a id="field-unknown-policy"></a>
## `unknown/policy`

- Required: `yes`
- Shape: enum: `deny`, `warn`, `allow`

<a id="field-evidence-complete-required"></a>
## `evidence/complete-required`

- Required: `yes`
- Shape: boolean
