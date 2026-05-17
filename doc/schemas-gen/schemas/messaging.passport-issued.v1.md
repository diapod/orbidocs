# Messaging Passport Issued v1

Source schema: [`doc/schemas/messaging.passport-issued.v1.schema.json`](../../schemas/messaging.passport-issued.v1.schema.json)

Messaging-owned Layer 3 fact recording issuance or refresh of a messaging-receive passport.

## Governing Basis

- [`doc/project/40-proposals/060-messaging-middleware.md`](../../project/40-proposals/060-messaging-middleware.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `messaging.passport-issued.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`fact/id`](#field-fact-id) | `yes` | string |  |
| [`event/at`](#field-event-at) | `yes` | string |  |
| [`passport/id`](#field-passport-id) | `yes` | string |  |
| [`capability/id`](#field-capability-id) | `yes` | const: `messaging-receive` |  |
| [`sender/subject`](#field-sender-subject) | `yes` | ref: `#/$defs/subject` |  |
| [`receiver/route`](#field-receiver-route) | `yes` | ref: `#/$defs/subject` |  |
| [`contact-request/id`](#field-contact-request-id) | `no` | string |  |
| [`contact-nym/id`](#field-contact-nym-id) | `no` | string |  |
| [`purpose`](#field-purpose) | `yes` | const: `messaging` |  |
| [`expires/at`](#field-expires-at) | `no` | string |  |
| [`revocation/ref`](#field-revocation-ref) | `no` | string \| null |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`subject`](#def-subject) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `messaging.passport-issued.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-fact-id"></a>
## `fact/id`

- Required: `yes`
- Shape: string

<a id="field-event-at"></a>
## `event/at`

- Required: `yes`
- Shape: string

<a id="field-passport-id"></a>
## `passport/id`

- Required: `yes`
- Shape: string

<a id="field-capability-id"></a>
## `capability/id`

- Required: `yes`
- Shape: const: `messaging-receive`

<a id="field-sender-subject"></a>
## `sender/subject`

- Required: `yes`
- Shape: ref: `#/$defs/subject`

<a id="field-receiver-route"></a>
## `receiver/route`

- Required: `yes`
- Shape: ref: `#/$defs/subject`

<a id="field-contact-request-id"></a>
## `contact-request/id`

- Required: `no`
- Shape: string

<a id="field-contact-nym-id"></a>
## `contact-nym/id`

- Required: `no`
- Shape: string

<a id="field-purpose"></a>
## `purpose`

- Required: `yes`
- Shape: const: `messaging`

<a id="field-expires-at"></a>
## `expires/at`

- Required: `no`
- Shape: string

<a id="field-revocation-ref"></a>
## `revocation/ref`

- Required: `no`
- Shape: string | null

## Definition Semantics

<a id="def-subject"></a>
## `$defs.subject`

- Shape: object
