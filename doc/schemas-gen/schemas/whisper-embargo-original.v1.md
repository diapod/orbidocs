# Whisper-embargo-original.v1

Source schema: [`doc/schemas/whisper-embargo-original.v1.schema.json`](../../schemas/whisper-embargo-original.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-embargo-original.v1` |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`certificate/digest`](#field-certificate-digest) | `yes` | string |  |
| [`context/digest`](#field-context-digest) | `yes` | string |  |
| [`epoch`](#field-epoch) | `yes` | integer |  |
| [`nym/id`](#field-nym-id) | `yes` | string |  |
| [`case/continuity-key-digest`](#field-case-continuity-key-digest) | `yes` | string |  |
| [`case/status-authority`](#field-case-status-authority) | `yes` | string |  |
| [`case/not-after`](#field-case-not-after) | `yes` | string |  |
| [`original/nonce`](#field-original-nonce) | `yes` | string |  |
| [`payload/commitment`](#field-payload-commitment) | `yes` | string |  |
| [`condition`](#field-condition) | `yes` | object |  |
| [`audiences`](#field-audiences) | `yes` | array |  |
| [`executors`](#field-executors) | `yes` | array |  |
| [`custody`](#field-custody) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-embargo-original.v1`

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-certificate-digest"></a>
## `certificate/digest`

- Required: `yes`
- Shape: string

<a id="field-context-digest"></a>
## `context/digest`

- Required: `yes`
- Shape: string

<a id="field-epoch"></a>
## `epoch`

- Required: `yes`
- Shape: integer

<a id="field-nym-id"></a>
## `nym/id`

- Required: `yes`
- Shape: string

<a id="field-case-continuity-key-digest"></a>
## `case/continuity-key-digest`

- Required: `yes`
- Shape: string

<a id="field-case-status-authority"></a>
## `case/status-authority`

- Required: `yes`
- Shape: string

<a id="field-case-not-after"></a>
## `case/not-after`

- Required: `yes`
- Shape: string

<a id="field-original-nonce"></a>
## `original/nonce`

- Required: `yes`
- Shape: string

<a id="field-payload-commitment"></a>
## `payload/commitment`

- Required: `yes`
- Shape: string

<a id="field-condition"></a>
## `condition`

- Required: `yes`
- Shape: object

<a id="field-audiences"></a>
## `audiences`

- Required: `yes`
- Shape: array

<a id="field-executors"></a>
## `executors`

- Required: `yes`
- Shape: array

<a id="field-custody"></a>
## `custody`

- Required: `yes`
- Shape: object
