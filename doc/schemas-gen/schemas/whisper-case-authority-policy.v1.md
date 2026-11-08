# Whisper-case-authority-policy.v1

Source schema: [`doc/schemas/whisper-case-authority-policy.v1.schema.json`](../../schemas/whisper-case-authority-policy.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/013-whisper-social-signal-exchange/private-case-continuity.md`](../../project/40-proposals/013-whisper-social-signal-exchange/private-case-continuity.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-case-authority-policy.v1` |  |
| [`authority/id`](#field-authority-id) | `yes` | string |  |
| [`federation/id`](#field-federation-id) | `yes` | string |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`case/max-lifetime-seconds`](#field-case-max-lifetime-seconds) | `yes` | integer |  |
| [`case/max-history-events`](#field-case-max-history-events) | `yes` | integer |  |
| [`case/max-active`](#field-case-max-active) | `yes` | integer |  |
| [`case/max-successions`](#field-case-max-successions) | `yes` | const: `64` |  |
| [`case/max-successions-per-day`](#field-case-max-successions-per-day) | `yes` | const: `4` |  |
| [`case/status-freshness-seconds`](#field-case-status-freshness-seconds) | `yes` | const: `300` |  |
| [`operations`](#field-operations) | `yes` | array |  |
| [`signature`](#field-signature) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-case-authority-policy.v1`

<a id="field-authority-id"></a>
## `authority/id`

- Required: `yes`
- Shape: string

<a id="field-federation-id"></a>
## `federation/id`

- Required: `yes`
- Shape: string

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

<a id="field-case-max-lifetime-seconds"></a>
## `case/max-lifetime-seconds`

- Required: `yes`
- Shape: integer

<a id="field-case-max-history-events"></a>
## `case/max-history-events`

- Required: `yes`
- Shape: integer

<a id="field-case-max-active"></a>
## `case/max-active`

- Required: `yes`
- Shape: integer

<a id="field-case-max-successions"></a>
## `case/max-successions`

- Required: `yes`
- Shape: const: `64`

<a id="field-case-max-successions-per-day"></a>
## `case/max-successions-per-day`

- Required: `yes`
- Shape: const: `4`

<a id="field-case-status-freshness-seconds"></a>
## `case/status-freshness-seconds`

- Required: `yes`
- Shape: const: `300`

<a id="field-operations"></a>
## `operations`

- Required: `yes`
- Shape: array

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object
