# Current Messaging Send Decision v1

Source schema: [`doc/schemas/messaging-send-decision.local.v1.schema.json`](../../schemas/messaging-send-decision.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md`](../../project/40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `messaging-send-decision.local.v1` |  |
| [`status`](#field-status) | `yes` | enum: `ready`, `blocked`, `unknown` |  |
| [`reasons`](#field-reasons) | `yes` | array |  |
| [`observed_at`](#field-observed-at) | `yes` | string |  |
| [`participant_id`](#field-participant-id) | `yes` | string |  |
| [`passport_id`](#field-passport-id) | `yes` | string \| null |  |
| [`evidence`](#field-evidence) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`provenance-reference`](#def-provenance-reference) | object |  |
| [`authority-failure`](#def-authority-failure) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `messaging-send-decision.local.v1`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `ready`, `blocked`, `unknown`

<a id="field-reasons"></a>
## `reasons`

- Required: `yes`
- Shape: array

<a id="field-observed-at"></a>
## `observed_at`

- Required: `yes`
- Shape: string

<a id="field-participant-id"></a>
## `participant_id`

- Required: `yes`
- Shape: string

<a id="field-passport-id"></a>
## `passport_id`

- Required: `yes`
- Shape: string | null

<a id="field-evidence"></a>
## `evidence`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-provenance-reference"></a>
## `$defs.provenance-reference`

- Shape: object

<a id="def-authority-failure"></a>
## `$defs.authority-failure`

- Shape: object
