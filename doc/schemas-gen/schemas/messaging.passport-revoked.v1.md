# Messaging Passport Revoked v1

Source schema: [`doc/schemas/messaging.passport-revoked.v1.schema.json`](../../schemas/messaging.passport-revoked.v1.schema.json)

Messaging-owned Layer 3 fact recording revocation of a messaging-receive passport.

## Governing Basis

- [`doc/project/40-proposals/060-messaging-middleware.md`](../../project/40-proposals/060-messaging-middleware.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `messaging.passport-revoked.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`fact/id`](#field-fact-id) | `yes` | string |  |
| [`event/at`](#field-event-at) | `yes` | string |  |
| [`passport/id`](#field-passport-id) | `yes` | string |  |
| [`capability/id`](#field-capability-id) | `yes` | const: `messaging-receive` |  |
| [`revocation/id`](#field-revocation-id) | `yes` | string |  |
| [`reason`](#field-reason) | `no` | string |  |
| [`source/ref`](#field-source-ref) | `no` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `messaging.passport-revoked.v1`

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

<a id="field-revocation-id"></a>
## `revocation/id`

- Required: `yes`
- Shape: string

<a id="field-reason"></a>
## `reason`

- Required: `no`
- Shape: string

<a id="field-source-ref"></a>
## `source/ref`

- Required: `no`
- Shape: string
