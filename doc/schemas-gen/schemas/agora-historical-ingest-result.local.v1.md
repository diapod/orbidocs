# Agora-historical-ingest-result.local.v1

Source schema: [`doc/schemas/agora-historical-ingest-result.local.v1.schema.json`](../../schemas/agora-historical-ingest-result.local.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agora-historical-ingest-result.local.v1` |  |
| [`record/id`](#field-record-id) | `yes` | string |  |
| [`local/admission`](#field-local-admission) | `yes` | enum: `live-issued`, `live-unwitnessed`, `historical-accepted` |  |
| [`duplicate`](#field-duplicate) | `yes` | boolean |  |
| [`sequence`](#field-sequence) | `yes` | integer |  |
| [`accepted/at`](#field-accepted-at) | `yes` | string |  |
| [`revocation/basis`](#field-revocation-basis) | `yes` | enum: `fresh-status`, `epoch-closure`, `revocation-interval` |  |
| [`revocation/basis-digest`](#field-revocation-basis-digest) | `yes` | string |  |
| [`signature/work`](#field-signature-work) | `yes` | integer |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agora-historical-ingest-result.local.v1`

<a id="field-record-id"></a>
## `record/id`

- Required: `yes`
- Shape: string

<a id="field-local-admission"></a>
## `local/admission`

- Required: `yes`
- Shape: enum: `live-issued`, `live-unwitnessed`, `historical-accepted`

<a id="field-duplicate"></a>
## `duplicate`

- Required: `yes`
- Shape: boolean

<a id="field-sequence"></a>
## `sequence`

- Required: `yes`
- Shape: integer

<a id="field-accepted-at"></a>
## `accepted/at`

- Required: `yes`
- Shape: string

<a id="field-revocation-basis"></a>
## `revocation/basis`

- Required: `yes`
- Shape: enum: `fresh-status`, `epoch-closure`, `revocation-interval`

<a id="field-revocation-basis-digest"></a>
## `revocation/basis-digest`

- Required: `yes`
- Shape: string

<a id="field-signature-work"></a>
## `signature/work`

- Required: `yes`
- Shape: integer
