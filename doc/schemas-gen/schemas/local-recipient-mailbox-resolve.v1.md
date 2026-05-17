# Local Recipient Mailbox Resolve v1

Source schema: [`doc/schemas/local-recipient-mailbox-resolve.v1.schema.json`](../../schemas/local-recipient-mailbox-resolve.v1.schema.json)

Host-capability request and response contract for local recipient mailbox resolution after message admission.

## Governing Basis

- [`doc/project/40-proposals/060-messaging-middleware.md`](../../project/40-proposals/060-messaging-middleware.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `local-recipient-mailbox-resolve.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`receiver/route`](#field-receiver-route) | `yes` | string |  |
| [`public-handle`](#field-public-handle) | `no` | object |  |
| [`purpose`](#field-purpose) | `yes` | const: `messaging` |  |
| [`freshness`](#field-freshness) | `no` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `local-recipient-mailbox-resolve.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-receiver-route"></a>
## `receiver/route`

- Required: `yes`
- Shape: string

<a id="field-public-handle"></a>
## `public-handle`

- Required: `no`
- Shape: object

<a id="field-purpose"></a>
## `purpose`

- Required: `yes`
- Shape: const: `messaging`

<a id="field-freshness"></a>
## `freshness`

- Required: `no`
- Shape: object
