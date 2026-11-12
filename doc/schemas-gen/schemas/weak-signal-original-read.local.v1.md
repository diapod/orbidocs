# Weak-signal-original-read.local.v1

Source schema: [`doc/schemas/weak-signal-original-read.local.v1.schema.json`](../../schemas/weak-signal-original-read.local.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`finding/id`](#field-finding-id) | `yes` | string |  |
| [`claim/id`](#field-claim-id) | `yes` | string |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |
| [`offset/bytes`](#field-offset-bytes) | `yes` | integer |  |
| [`length/bytes`](#field-length-bytes) | `yes` | integer |  |
## Field Semantics

<a id="field-finding-id"></a>
## `finding/id`

- Required: `yes`
- Shape: string

<a id="field-claim-id"></a>
## `claim/id`

- Required: `yes`
- Shape: string

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

<a id="field-offset-bytes"></a>
## `offset/bytes`

- Required: `yes`
- Shape: integer

<a id="field-length-bytes"></a>
## `length/bytes`

- Required: `yes`
- Shape: integer
