# Whisper-embargo-audience-manifest.v1

Source schema: [`doc/schemas/whisper-embargo-audience-manifest.v1.schema.json`](../../schemas/whisper-embargo-audience-manifest.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-embargo-audience-manifest.v1` |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`certificate/digest`](#field-certificate-digest) | `yes` | string |  |
| [`context/digest`](#field-context-digest) | `yes` | string |  |
| [`epoch`](#field-epoch) | `yes` | integer |  |
| [`nym/id`](#field-nym-id) | `yes` | string |  |
| [`case/continuity-key-digest`](#field-case-continuity-key-digest) | `yes` | string |  |
| [`case/status-authority`](#field-case-status-authority) | `yes` | string |  |
| [`case/not-after`](#field-case-not-after) | `yes` | string |  |
| [`condition/original`](#field-condition-original) | `yes` | string |  |
| [`payload/commitment`](#field-payload-commitment) | `yes` | string |  |
| [`condition`](#field-condition) | `yes` | object |  |
| [`audience`](#field-audience) | `yes` | ref: `room-release-audience.v1.schema.json` |  |
| [`executors`](#field-executors) | `yes` | array |  |
| [`manifest/nonce`](#field-manifest-nonce) | `yes` | string |  |
| [`publication/context`](#field-publication-context) | `yes` | object |  |
| [`signature`](#field-signature) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-embargo-audience-manifest.v1`

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

<a id="field-condition-original"></a>
## `condition/original`

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

<a id="field-audience"></a>
## `audience`

- Required: `yes`
- Shape: ref: `room-release-audience.v1.schema.json`

<a id="field-executors"></a>
## `executors`

- Required: `yes`
- Shape: array

<a id="field-manifest-nonce"></a>
## `manifest/nonce`

- Required: `yes`
- Shape: string

<a id="field-publication-context"></a>
## `publication/context`

- Required: `yes`
- Shape: object

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: string
