# Agora-admission-inspection.local.v2

Source schema: [`doc/schemas/agora-admission-inspection.local.v2.schema.json`](../../schemas/agora-admission-inspection.local.v2.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agora-admission-inspection.local.v2` |  |
| [`inputs/digest`](#field-inputs-digest) | `yes` | string |  |
| [`result/digest`](#field-result-digest) | `yes` | string |  |
| [`evaluated_at`](#field-evaluated-at) | `yes` | string |  |
| [`receipt/profile`](#field-receipt-profile) | `yes` | enum: `full-record`, `detached-manifest` |  |
| [`record/authenticity`](#field-record-authenticity) | `yes` | object |  |
| [`receipt/authenticity`](#field-receipt-authenticity) | `yes` | object |  |
| [`historical/admission`](#field-historical-admission) | `yes` | object |  |
| [`current/status`](#field-current-status) | `yes` | object |  |
| [`basis`](#field-basis) | `yes` | const: `admission-snapshot` |  |
| [`compromise`](#field-compromise) | `yes` | const: `not-assessable` |  |
| [`revocation/ordering`](#field-revocation-ordering) | `yes` | enum: `before`, `after`, `unknown`, `none-observed` |  |
| [`receipts`](#field-receipts) | `yes` | array |  |
| [`issuance`](#field-issuance) | `yes` | unspecified |  |
| [`verification/signature-work`](#field-verification-signature-work) | `yes` | integer |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agora-admission-inspection.local.v2`

<a id="field-inputs-digest"></a>
## `inputs/digest`

- Required: `yes`
- Shape: string

<a id="field-result-digest"></a>
## `result/digest`

- Required: `yes`
- Shape: string

<a id="field-evaluated-at"></a>
## `evaluated_at`

- Required: `yes`
- Shape: string

<a id="field-receipt-profile"></a>
## `receipt/profile`

- Required: `yes`
- Shape: enum: `full-record`, `detached-manifest`

<a id="field-record-authenticity"></a>
## `record/authenticity`

- Required: `yes`
- Shape: object

<a id="field-receipt-authenticity"></a>
## `receipt/authenticity`

- Required: `yes`
- Shape: object

<a id="field-historical-admission"></a>
## `historical/admission`

- Required: `yes`
- Shape: object

<a id="field-current-status"></a>
## `current/status`

- Required: `yes`
- Shape: object

<a id="field-basis"></a>
## `basis`

- Required: `yes`
- Shape: const: `admission-snapshot`

<a id="field-compromise"></a>
## `compromise`

- Required: `yes`
- Shape: const: `not-assessable`

<a id="field-revocation-ordering"></a>
## `revocation/ordering`

- Required: `yes`
- Shape: enum: `before`, `after`, `unknown`, `none-observed`

<a id="field-receipts"></a>
## `receipts`

- Required: `yes`
- Shape: array

<a id="field-issuance"></a>
## `issuance`

- Required: `yes`
- Shape: unspecified

<a id="field-verification-signature-work"></a>
## `verification/signature-work`

- Required: `yes`
- Shape: integer
