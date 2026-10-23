# Scheduled-module-job-request.v1

Source schema: [`doc/schemas/scheduled-module-job-request.v1.schema.json`](../../schemas/scheduled-module-job-request.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `scheduled-module-job-request.v1` |  |
| [`job/id`](#field-job-id) | `yes` | string |  |
| [`launch/id`](#field-launch-id) | `yes` | string |  |
| [`owner/module-id`](#field-owner-module-id) | `yes` | string |  |
| [`operation`](#field-operation) | `yes` | string |  |
| [`scheduled/for-ms`](#field-scheduled-for-ms) | `yes` | integer |  |
| [`started/at-ms`](#field-started-at-ms) | `yes` | integer |  |
| [`budget/remaining-ms`](#field-budget-remaining-ms) | `yes` | integer | Upper bound in milliseconds for the module response and all launch-owned work. The module MUST finish before this budget expires, including child cleanup. A host timeout does not establish cancellation or absence of effects. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `scheduled-module-job-request.v1`

<a id="field-job-id"></a>
## `job/id`

- Required: `yes`
- Shape: string

<a id="field-launch-id"></a>
## `launch/id`

- Required: `yes`
- Shape: string

<a id="field-owner-module-id"></a>
## `owner/module-id`

- Required: `yes`
- Shape: string

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: string

<a id="field-scheduled-for-ms"></a>
## `scheduled/for-ms`

- Required: `yes`
- Shape: integer

<a id="field-started-at-ms"></a>
## `started/at-ms`

- Required: `yes`
- Shape: integer

<a id="field-budget-remaining-ms"></a>
## `budget/remaining-ms`

- Required: `yes`
- Shape: integer

Upper bound in milliseconds for the module response and all launch-owned work. The module MUST finish before this budget expires, including child cleanup. A host timeout does not establish cancellation or absence of effects.
