# Whisper-release-intent.v1

Source schema: [`doc/schemas/whisper-release-intent.v1.schema.json`](../../schemas/whisper-release-intent.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-release-intent.v1` |  |
| [`release/id`](#field-release-id) | `yes` | string |  |
| [`condition/original`](#field-condition-original) | `yes` | string |  |
| [`manifest/digest`](#field-manifest-digest) | `yes` | string |  |
| [`payload/commitment`](#field-payload-commitment) | `yes` | string |  |
| [`audience`](#field-audience) | `yes` | ref: `room-release-audience.v1.schema.json` |  |
| [`executor`](#field-executor) | `yes` | string |  |
| [`handover/by`](#field-handover-by) | `yes` | integer |  |
| [`public/envelope`](#field-public-envelope) | `yes` | object |  |
| [`proof/package-digest`](#field-proof-package-digest) | `yes` | string |  |
| [`execution/commitment`](#field-execution-commitment) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-release-intent.v1`

<a id="field-release-id"></a>
## `release/id`

- Required: `yes`
- Shape: string

<a id="field-condition-original"></a>
## `condition/original`

- Required: `yes`
- Shape: string

<a id="field-manifest-digest"></a>
## `manifest/digest`

- Required: `yes`
- Shape: string

<a id="field-payload-commitment"></a>
## `payload/commitment`

- Required: `yes`
- Shape: string

<a id="field-audience"></a>
## `audience`

- Required: `yes`
- Shape: ref: `room-release-audience.v1.schema.json`

<a id="field-executor"></a>
## `executor`

- Required: `yes`
- Shape: string

<a id="field-handover-by"></a>
## `handover/by`

- Required: `yes`
- Shape: integer

<a id="field-public-envelope"></a>
## `public/envelope`

- Required: `yes`
- Shape: object

<a id="field-proof-package-digest"></a>
## `proof/package-digest`

- Required: `yes`
- Shape: string

<a id="field-execution-commitment"></a>
## `execution/commitment`

- Required: `yes`
- Shape: string
