# Whisper-case-acceptance.v1

Source schema: [`doc/schemas/whisper-case-acceptance.v1.schema.json`](../../schemas/whisper-case-acceptance.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-case-acceptance.v1` |  |
| [`case/anchor`](#field-case-anchor) | `yes` | string |  |
| [`case/authority`](#field-case-authority) | `yes` | string |  |
| [`request/digest`](#field-request-digest) | `yes` | string |  |
| [`case/previous`](#field-case-previous) | `yes` | string |  |
| [`operation`](#field-operation) | `yes` | enum: `register`, `succession`, `amendment`, `withdrawal`, `confirmation`, `closure`, `release-commit`, `abandonment`, `anchor-invalidated` |  |
| [`accepted/at`](#field-accepted-at) | `yes` | string |  |
| [`inputs/digest`](#field-inputs-digest) | `yes` | string |  |
| [`head`](#field-head) | `yes` | object |  |
| [`anchor/basis`](#field-anchor-basis) | `yes` | enum: `after`, `none-observed-closed`, `none-observed-fresh`, `None` |  |
| [`signature`](#field-signature) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-case-acceptance.v1`

<a id="field-case-anchor"></a>
## `case/anchor`

- Required: `yes`
- Shape: string

<a id="field-case-authority"></a>
## `case/authority`

- Required: `yes`
- Shape: string

<a id="field-request-digest"></a>
## `request/digest`

- Required: `yes`
- Shape: string

<a id="field-case-previous"></a>
## `case/previous`

- Required: `yes`
- Shape: string

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: enum: `register`, `succession`, `amendment`, `withdrawal`, `confirmation`, `closure`, `release-commit`, `abandonment`, `anchor-invalidated`

<a id="field-accepted-at"></a>
## `accepted/at`

- Required: `yes`
- Shape: string

<a id="field-inputs-digest"></a>
## `inputs/digest`

- Required: `yes`
- Shape: string

<a id="field-head"></a>
## `head`

- Required: `yes`
- Shape: object

<a id="field-anchor-basis"></a>
## `anchor/basis`

- Required: `yes`
- Shape: enum: `after`, `none-observed-closed`, `none-observed-fresh`, `None`

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: string
