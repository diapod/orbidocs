# Story-012-delegated-adaptive-executor-profile.v1

Source schema: [`doc/schemas/story-012-delegated-adaptive-executor-profile.v1.schema.json`](../../schemas/story-012-delegated-adaptive-executor-profile.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `story-012-delegated-adaptive-executor-profile.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`profile/id`](#field-profile-id) | `yes` | const: `story-012-delegated-adaptive-executor` |  |
| [`source/report`](#field-source-report) | `yes` | string |  |
| [`source/report/sha256`](#field-source-report-sha256) | `yes` | string |  |
| [`requester/node`](#field-requester-node) | `yes` | const: `node-a` |  |
| [`executor/designation`](#field-executor-designation) | `yes` | object |  |
| [`required/invariants`](#field-required-invariants) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `story-012-delegated-adaptive-executor-profile.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-profile-id"></a>
## `profile/id`

- Required: `yes`
- Shape: const: `story-012-delegated-adaptive-executor`

<a id="field-source-report"></a>
## `source/report`

- Required: `yes`
- Shape: string

<a id="field-source-report-sha256"></a>
## `source/report/sha256`

- Required: `yes`
- Shape: string

<a id="field-requester-node"></a>
## `requester/node`

- Required: `yes`
- Shape: const: `node-a`

<a id="field-executor-designation"></a>
## `executor/designation`

- Required: `yes`
- Shape: object

<a id="field-required-invariants"></a>
## `required/invariants`

- Required: `yes`
- Shape: array
