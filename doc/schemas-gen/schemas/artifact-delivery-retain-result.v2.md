# Artifact-delivery-retain-result.v2

Source schema: [`doc/schemas/artifact-delivery-retain-result.v2.schema.json`](../../schemas/artifact-delivery-retain-result.v2.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `artifact-delivery-retain-result.v2` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `2` |  |
| [`outcome`](#field-outcome) | `yes` | const: `completed` |  |
| [`claim`](#field-claim) | `yes` | object |  |
| [`retained/at`](#field-retained-at) | `yes` | string |  |
| [`effective/until`](#field-effective-until) | `yes` | string |  |
| [`policy/ref`](#field-policy-ref) | `yes` | string |  |
| [`artifact/digest`](#field-artifact-digest) | `yes` | string |  |
| [`artifact/size-bytes`](#field-artifact-size-bytes) | `yes` | integer |  |
| [`execution/receipt`](#field-execution-receipt) | `yes` | ref: `execution-receipt.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `artifact-delivery-retain-result.v2`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `2`

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: const: `completed`

<a id="field-claim"></a>
## `claim`

- Required: `yes`
- Shape: object

<a id="field-retained-at"></a>
## `retained/at`

- Required: `yes`
- Shape: string

<a id="field-effective-until"></a>
## `effective/until`

- Required: `yes`
- Shape: string

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `yes`
- Shape: string

<a id="field-artifact-digest"></a>
## `artifact/digest`

- Required: `yes`
- Shape: string

<a id="field-artifact-size-bytes"></a>
## `artifact/size-bytes`

- Required: `yes`
- Shape: integer

<a id="field-execution-receipt"></a>
## `execution/receipt`

- Required: `yes`
- Shape: ref: `execution-receipt.v1.schema.json`
