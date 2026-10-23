# Scheduled-module-job-result.v1

Source schema: [`doc/schemas/scheduled-module-job-result.v1.schema.json`](../../schemas/scheduled-module-job-result.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `scheduled-module-job-result.v1` |  |
| [`job/id`](#field-job-id) | `yes` | string |  |
| [`launch/id`](#field-launch-id) | `yes` | string |  |
| [`status`](#field-status) | `yes` | enum: `completed`, `no-work`, `blocked` |  |
| [`records/seen`](#field-records-seen) | `yes` | integer |  |
| [`details`](#field-details) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `scheduled-module-job-result.v1`

<a id="field-job-id"></a>
## `job/id`

- Required: `yes`
- Shape: string

<a id="field-launch-id"></a>
## `launch/id`

- Required: `yes`
- Shape: string

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `completed`, `no-work`, `blocked`

<a id="field-records-seen"></a>
## `records/seen`

- Required: `yes`
- Shape: integer

<a id="field-details"></a>
## `details`

- Required: `yes`
- Shape: object
