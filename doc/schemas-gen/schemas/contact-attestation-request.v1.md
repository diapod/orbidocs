# Contact Attestation Request v1

Source schema: [`doc/schemas/contact-attestation-request.v1.schema.json`](../../schemas/contact-attestation-request.v1.schema.json)

Acquisition-side request from a node to a contact attestation service asking it to challenge one email address or phone number and later issue a contact-control passport.

## Governing Basis

- [`doc/project/40-proposals/061-contact-attestation-service.md`](../../project/40-proposals/061-contact-attestation-service.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `contact-attestation-request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`request/id`](#field-request-id) | `yes` | string |  |
| [`contact/kind`](#field-contact-kind) | `yes` | enum: `email`, `phone` |  |
| [`contact/value`](#field-contact-value) | `yes` | string | Raw delivery target. It is sent only to the selected attestation service. |
| [`subject`](#field-subject) | `yes` | ref: `#/$defs/subject` |  |
| [`requested/capability-id`](#field-requested-capability-id) | `yes` | enum: `email-control`, `phone-control` |  |
| [`requested/profile`](#field-requested-profile) | `yes` | enum: `email-control@v1`, `phone-control@v1` |  |
| [`requested/purposes`](#field-requested-purposes) | `yes` | array |  |
| [`delivery/preference`](#field-delivery-preference) | `no` | enum: `link-and-code`, `code-only` |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `no` | string |  |
| [`proof/signature`](#field-proof-signature) | `no` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`subject`](#def-subject) | object |  |
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `contact-attestation-request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-request-id"></a>
## `request/id`

- Required: `yes`
- Shape: string

<a id="field-contact-kind"></a>
## `contact/kind`

- Required: `yes`
- Shape: enum: `email`, `phone`

<a id="field-contact-value"></a>
## `contact/value`

- Required: `yes`
- Shape: string

Raw delivery target. It is sent only to the selected attestation service.

<a id="field-subject"></a>
## `subject`

- Required: `yes`
- Shape: ref: `#/$defs/subject`

<a id="field-requested-capability-id"></a>
## `requested/capability-id`

- Required: `yes`
- Shape: enum: `email-control`, `phone-control`

<a id="field-requested-profile"></a>
## `requested/profile`

- Required: `yes`
- Shape: enum: `email-control@v1`, `phone-control@v1`

<a id="field-requested-purposes"></a>
## `requested/purposes`

- Required: `yes`
- Shape: array

<a id="field-delivery-preference"></a>
## `delivery/preference`

- Required: `no`
- Shape: enum: `link-and-code`, `code-only`

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `no`
- Shape: string

<a id="field-proof-signature"></a>
## `proof/signature`

- Required: `no`
- Shape: ref: `#/$defs/signature`

## Definition Semantics

<a id="def-subject"></a>
## `$defs.subject`

- Shape: object

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
