# Bounded HTTP Fetch Operator Snapshot v1

Source schema: [`doc/schemas/bounded-http-fetch-operator-snapshot.v1.schema.json`](../../schemas/bounded-http-fetch-operator-snapshot.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `bounded-http-fetch-operator-snapshot.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`status`](#field-status) | `yes` | enum: `ready`, `degraded`, `unavailable` |  |
| [`active`](#field-active) | `yes` | integer |  |
| [`capacity`](#field-capacity) | `yes` | integer |  |
| [`requests/total`](#field-requests-total) | `yes` | integer | All calls reaching the fetch-service execute boundary, including typed requests rejected by contract validation or policy admission. |
| [`completed/total`](#field-completed-total) | `yes` | integer |  |
| [`refused/total`](#field-refused-total) | `yes` | integer |  |
| [`failed/total`](#field-failed-total) | `yes` | integer |  |
| [`artifact-handoffs/total`](#field-artifact-handoffs-total) | `yes` | integer |  |
| [`failure-counts`](#field-failure-counts) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `bounded-http-fetch-operator-snapshot.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `ready`, `degraded`, `unavailable`

<a id="field-active"></a>
## `active`

- Required: `yes`
- Shape: integer

<a id="field-capacity"></a>
## `capacity`

- Required: `yes`
- Shape: integer

<a id="field-requests-total"></a>
## `requests/total`

- Required: `yes`
- Shape: integer

All calls reaching the fetch-service execute boundary, including typed requests rejected by contract validation or policy admission.

<a id="field-completed-total"></a>
## `completed/total`

- Required: `yes`
- Shape: integer

<a id="field-refused-total"></a>
## `refused/total`

- Required: `yes`
- Shape: integer

<a id="field-failed-total"></a>
## `failed/total`

- Required: `yes`
- Shape: integer

<a id="field-artifact-handoffs-total"></a>
## `artifact-handoffs/total`

- Required: `yes`
- Shape: integer

<a id="field-failure-counts"></a>
## `failure-counts`

- Required: `yes`
- Shape: object
