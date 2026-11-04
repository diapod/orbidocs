# Artifact-delivery-retain-request.v2

Source schema: [`doc/schemas/artifact-delivery-retain-request.v2.schema.json`](../../schemas/artifact-delivery-retain-request.v2.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `artifact-delivery-retain-request.v2` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `2` |  |
| [`owner/component-id`](#field-owner-component-id) | `yes` | string |  |
| [`purpose`](#field-purpose) | `yes` | string |  |
| [`snapshot/ref`](#field-snapshot-ref) | `yes` | string |  |
| [`artifact`](#field-artifact) | `yes` | object |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |
| [`causal/context`](#field-causal-context) | `yes` | ref: `causal-context.v1.schema.json` |  |
| [`requested-retention/seconds`](#field-requested-retention-seconds) | `no` | integer |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `artifact-delivery-retain-request.v2`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `2`

<a id="field-owner-component-id"></a>
## `owner/component-id`

- Required: `yes`
- Shape: string

<a id="field-purpose"></a>
## `purpose`

- Required: `yes`
- Shape: string

<a id="field-snapshot-ref"></a>
## `snapshot/ref`

- Required: `yes`
- Shape: string

<a id="field-artifact"></a>
## `artifact`

- Required: `yes`
- Shape: object

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

<a id="field-causal-context"></a>
## `causal/context`

- Required: `yes`
- Shape: ref: `causal-context.v1.schema.json`

<a id="field-requested-retention-seconds"></a>
## `requested-retention/seconds`

- Required: `no`
- Shape: integer
