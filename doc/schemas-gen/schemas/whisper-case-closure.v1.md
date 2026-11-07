# Whisper-case-closure.v1

Source schema: [`doc/schemas/whisper-case-closure.v1.schema.json`](../../schemas/whisper-case-closure.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-case-closure.v1` |  |
| [`case/anchor`](#field-case-anchor) | `yes` | string |  |
| [`request/id`](#field-request-id) | `yes` | string |  |
| [`not-after`](#field-not-after) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | string |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`closure/reason`](#field-closure-reason) | `yes` | enum: `author-ended`, `key-compromise-suspected` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-case-closure.v1`

<a id="field-case-anchor"></a>
## `case/anchor`

- Required: `yes`
- Shape: string

<a id="field-request-id"></a>
## `request/id`

- Required: `yes`
- Shape: string

<a id="field-not-after"></a>
## `not-after`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

<a id="field-closure-reason"></a>
## `closure/reason`

- Required: `yes`
- Shape: enum: `author-ended`, `key-compromise-suspected`
