# Messaging-mailbox-storage.local.v1

Source schema: [`doc/schemas/messaging-mailbox-storage.local.v1.schema.json`](../../schemas/messaging-mailbox-storage.local.v1.schema.json)

Layer 1 local mailbox identity; filesystem slugs are not logical mailbox identifiers.

## Governing Basis

- [`doc/project/60-solutions/027-messaging-middleware/027-messaging-middleware.md`](../../project/60-solutions/027-messaging-middleware/027-messaging-middleware.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `messaging-mailbox-storage.local.v1` |  |
| [`mailbox/id`](#field-mailbox-id) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `messaging-mailbox-storage.local.v1`

<a id="field-mailbox-id"></a>
## `mailbox/id`

- Required: `yes`
- Shape: string
