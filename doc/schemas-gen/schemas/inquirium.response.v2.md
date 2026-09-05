# Provenance-bearing Inquirium Response

Source schema: [`doc/schemas/inquirium.response.v2.schema.json`](../../schemas/inquirium.response.v2.schema.json)

Compatible envelope around an exact operation response. The operation owner additionally validates the enclosed response and content binding; this envelope grants no execution authority.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inquirium.response.v2` |  |
| [`response`](#field-response) | `yes` | object | The operation owner validates this payload against its own versioned response contract. |
| [`result/provenance`](#field-result-provenance) | `yes` | ref: `inquirium.result-provenance.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.response.v2`

<a id="field-response"></a>
## `response`

- Required: `yes`
- Shape: object

The operation owner validates this payload against its own versioned response contract.

<a id="field-result-provenance"></a>
## `result/provenance`

- Required: `yes`
- Shape: ref: `inquirium.result-provenance.v1.schema.json`
