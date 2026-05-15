# Notification State Changed v1

Source schema: [`doc/schemas/notification-state-changed.v1.schema.json`](../../schemas/notification-state-changed.v1.schema.json)

Privacy-minimal SSE payload announcing that a recipient notification read model changed. It intentionally excludes title, body, kind, subject, actions, and raw input.

## Governing Basis

- [`doc/project/40-proposals/057-user-and-operator-notifications.md`](../../project/40-proposals/057-user-and-operator-notifications.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `notification-state-changed.v1` |  |
| [`recipient/id`](#field-recipient-id) | `yes` | string |  |
| [`notification/id`](#field-notification-id) | `no` | string |  |
| [`unread/count`](#field-unread-count) | `yes` | integer |  |
| [`max/unread-priority`](#field-max-unread-priority) | `yes` | integer |  |
| [`last/changed-at`](#field-last-changed-at) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `notification-state-changed.v1`

<a id="field-recipient-id"></a>
## `recipient/id`

- Required: `yes`
- Shape: string

<a id="field-notification-id"></a>
## `notification/id`

- Required: `no`
- Shape: string

<a id="field-unread-count"></a>
## `unread/count`

- Required: `yes`
- Shape: integer

<a id="field-max-unread-priority"></a>
## `max/unread-priority`

- Required: `yes`
- Shape: integer

<a id="field-last-changed-at"></a>
## `last/changed-at`

- Required: `yes`
- Shape: string
