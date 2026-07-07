# Operator-consent-binding.v1

Source schema: [`doc/schemas/operator-consent-binding.v1.schema.json`](../../schemas/operator-consent-binding.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-consent-binding.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`approval/ref`](#field-approval-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`operator/ref`](#field-operator-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`issued/at`](#field-issued-at) | `yes` | ref: `#/$defs/timestamp` |  |
| [`expires/at`](#field-expires-at) | `no` | unspecified |  |
| [`revocation/ref`](#field-revocation-ref) | `no` | unspecified |  |
| [`delta/digest`](#field-delta-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`operation/ref`](#field-operation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`capability/id`](#field-capability-id) | `yes` | ref: `#/$defs/capability_id` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`capability_id`](#def-capability-id) | string |  |
| [`digest`](#def-digest) | string |  |
| [`ref`](#def-ref) | string |  |
| [`timestamp`](#def-timestamp) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-consent-binding.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-approval-ref"></a>
## `approval/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-operator-ref"></a>
## `operator/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: ref: `#/$defs/timestamp`

<a id="field-expires-at"></a>
## `expires/at`

- Required: `no`
- Shape: unspecified

<a id="field-revocation-ref"></a>
## `revocation/ref`

- Required: `no`
- Shape: unspecified

<a id="field-delta-digest"></a>
## `delta/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-operation-ref"></a>
## `operation/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-capability-id"></a>
## `capability/id`

- Required: `yes`
- Shape: ref: `#/$defs/capability_id`

## Definition Semantics

<a id="def-capability-id"></a>
## `$defs.capability_id`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-timestamp"></a>
## `$defs.timestamp`

- Shape: string
