# Contact Attestation Result v1

Source schema: [`doc/schemas/contact-attestation-result.v1.schema.json`](../../schemas/contact-attestation-result.v1.schema.json)

Return artifact produced after a successful contact attestation challenge redemption. It carries the issued email-control@v1 or phone-control@v1 passport.

## Governing Basis

- [`doc/project/40-proposals/061-contact-attestation-service.md`](../../project/40-proposals/061-contact-attestation-service.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `contact-attestation-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`request/id`](#field-request-id) | `yes` | string |  |
| [`challenge/id`](#field-challenge-id) | `yes` | string |  |
| [`contact/kind`](#field-contact-kind) | `yes` | enum: `email`, `phone` |  |
| [`contact/digest`](#field-contact-digest) | `yes` | string |  |
| [`passport`](#field-passport) | `yes` | object | Issued capability-passport.v1 artifact for email-control@v1 or phone-control@v1. |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `no` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `contact-attestation-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-request-id"></a>
## `request/id`

- Required: `yes`
- Shape: string

<a id="field-challenge-id"></a>
## `challenge/id`

- Required: `yes`
- Shape: string

<a id="field-contact-kind"></a>
## `contact/kind`

- Required: `yes`
- Shape: enum: `email`, `phone`

<a id="field-contact-digest"></a>
## `contact/digest`

- Required: `yes`
- Shape: string

<a id="field-passport"></a>
## `passport`

- Required: `yes`
- Shape: object

Issued capability-passport.v1 artifact for email-control@v1 or phone-control@v1.

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `no`
- Shape: string
