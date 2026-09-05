# Inference Policy Evaluation Request v1

Source schema: [`doc/schemas/inference-policy.evaluate.request.v1.schema.json`](../../schemas/inference-policy.evaluate.request.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inference-policy.evaluate.request.v1` |  |
| [`policy`](#field-policy) | `yes` | ref: `inference-consumption-policy.v1.schema.json` |  |
| [`at`](#field-at) | `yes` | string |  |
| [`subjects`](#field-subjects) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inference-policy.evaluate.request.v1`

<a id="field-policy"></a>
## `policy`

- Required: `yes`
- Shape: ref: `inference-consumption-policy.v1.schema.json`

<a id="field-at"></a>
## `at`

- Required: `yes`
- Shape: string

<a id="field-subjects"></a>
## `subjects`

- Required: `yes`
- Shape: array
