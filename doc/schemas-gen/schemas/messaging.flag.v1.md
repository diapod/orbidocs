# Messaging Flag v1

Source schema: [`doc/schemas/messaging.flag.v1.schema.json`](../../schemas/messaging.flag.v1.schema.json)

Messaging-owned Layer 3 fact recording a replayable local message flag change, such as read/unread.

## Governing Basis

- [`doc/project/40-proposals/060-messaging-middleware.md`](../../project/40-proposals/060-messaging-middleware.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `messaging.flag.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`fact/id`](#field-fact-id) | `yes` | string |  |
| [`event/at`](#field-event-at) | `yes` | string |  |
| [`message/id`](#field-message-id) | `yes` | string |  |
| [`mailbox/id`](#field-mailbox-id) | `yes` | string |  |
| [`flag/name`](#field-flag-name) | `yes` | enum: `read` |  |
| [`flag/state`](#field-flag-state) | `yes` | enum: `set`, `cleared` |  |
| [`actor/ref`](#field-actor-ref) | `yes` | string |  |
| [`source/device-id`](#field-source-device-id) | `no` | string |  |
| [`causation/ref`](#field-causation-ref) | `no` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `messaging.flag.v1`

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

<a id="field-message-id"></a>
## `message/id`

- Required: `yes`
- Shape: string

<a id="field-mailbox-id"></a>
## `mailbox/id`

- Required: `yes`
- Shape: string

<a id="field-flag-name"></a>
## `flag/name`

- Required: `yes`
- Shape: enum: `read`

<a id="field-flag-state"></a>
## `flag/state`

- Required: `yes`
- Shape: enum: `set`, `cleared`

<a id="field-actor-ref"></a>
## `actor/ref`

- Required: `yes`
- Shape: string

<a id="field-source-device-id"></a>
## `source/device-id`

- Required: `no`
- Shape: string

<a id="field-causation-ref"></a>
## `causation/ref`

- Required: `no`
- Shape: string
