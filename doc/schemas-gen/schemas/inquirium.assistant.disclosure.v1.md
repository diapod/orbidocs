# Exact Assistant Pre-execution Disclosure

Source schema: [`doc/schemas/inquirium.assistant.disclosure.v1.schema.json`](../../schemas/inquirium.assistant.disclosure.v1.schema.json)

Host-authenticated view of one prepared invocation. Neither the view nor acknowledgement grants inference or context authority.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inquirium.assistant.disclosure.v1` |  |
| [`principal/ref`](#field-principal-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`session/ref`](#field-session-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`request/binding`](#field-request-binding) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`plan/binding`](#field-plan-binding) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`runtime/ref`](#field-runtime-ref) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
| [`configuration/digest`](#field-configuration-digest) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/digest` |  |
| [`posture`](#field-posture) | `yes` | unspecified |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |
| [`expires/at-epoch-seconds`](#field-expires-at-epoch-seconds) | `yes` | integer |  |
| [`acknowledgement/required`](#field-acknowledgement-required) | `yes` | boolean |  |
| [`token`](#field-token) | `yes` | ref: `inference-provenance-common.v1.schema.json#/$defs/ref` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.assistant.disclosure.v1`

<a id="field-principal-ref"></a>
## `principal/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-session-ref"></a>
## `session/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-request-binding"></a>
## `request/binding`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-plan-binding"></a>
## `plan/binding`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-runtime-ref"></a>
## `runtime/ref`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`

<a id="field-configuration-digest"></a>
## `configuration/digest`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/digest`

<a id="field-posture"></a>
## `posture`

- Required: `yes`
- Shape: unspecified

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

<a id="field-expires-at-epoch-seconds"></a>
## `expires/at-epoch-seconds`

- Required: `yes`
- Shape: integer

<a id="field-acknowledgement-required"></a>
## `acknowledgement/required`

- Required: `yes`
- Shape: boolean

<a id="field-token"></a>
## `token`

- Required: `yes`
- Shape: ref: `inference-provenance-common.v1.schema.json#/$defs/ref`
