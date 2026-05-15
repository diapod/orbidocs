# Notification Create v1

Source schema: [`doc/schemas/notification-create.v1.schema.json`](../../schemas/notification-create.v1.schema.json)

Host capability request used by authorized producers to create a durable local notification. Raw body/input is transient request material and MUST NOT be persisted.

## Governing Basis

- [`doc/project/40-proposals/057-user-and-operator-notifications.md`](../../project/40-proposals/057-user-and-operator-notifications.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `notification-create.v1` |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`notification/kind`](#field-notification-kind) | `yes` | string |  |
| [`correlation/id`](#field-correlation-id) | `no` | string |  |
| [`collapse/key`](#field-collapse-key) | `no` | string |  |
| [`sender/ref`](#field-sender-ref) | `no` | string |  |
| [`recipient/class`](#field-recipient-class) | `yes` | ref: `#/$defs/recipientClass` |  |
| [`recipient/id`](#field-recipient-id) | `no` | string |  |
| [`subject/ref`](#field-subject-ref) | `no` | string |  |
| [`priority`](#field-priority) | `yes` | ref: `#/$defs/priority` |  |
| [`reason/code`](#field-reason-code) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `no` | string |  |
| [`title`](#field-title) | `yes` | string |  |
| [`body/text`](#field-body-text) | `no` | string |  |
| [`body/ref`](#field-body-ref) | `no` | string |  |
| [`body/input`](#field-body-input) | `no` | unspecified | Transient producer input used only for validation, action rendering context, or digesting. It MUST NOT be persisted by the notification store. |
| [`actions`](#field-actions) | `no` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`priority`](#def-priority) | enum: `low`, `medium`, `high` |  |
| [`recipientClass`](#def-recipientclass) | enum: `operator`, `user`, `pod-user`, `role` |  |
| [`action`](#def-action) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `notification-create.v1`

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string

<a id="field-notification-kind"></a>
## `notification/kind`

- Required: `yes`
- Shape: string

<a id="field-correlation-id"></a>
## `correlation/id`

- Required: `no`
- Shape: string

<a id="field-collapse-key"></a>
## `collapse/key`

- Required: `no`
- Shape: string

<a id="field-sender-ref"></a>
## `sender/ref`

- Required: `no`
- Shape: string

<a id="field-recipient-class"></a>
## `recipient/class`

- Required: `yes`
- Shape: ref: `#/$defs/recipientClass`

<a id="field-recipient-id"></a>
## `recipient/id`

- Required: `no`
- Shape: string

<a id="field-subject-ref"></a>
## `subject/ref`

- Required: `no`
- Shape: string

<a id="field-priority"></a>
## `priority`

- Required: `yes`
- Shape: ref: `#/$defs/priority`

<a id="field-reason-code"></a>
## `reason/code`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `no`
- Shape: string

<a id="field-title"></a>
## `title`

- Required: `yes`
- Shape: string

<a id="field-body-text"></a>
## `body/text`

- Required: `no`
- Shape: string

<a id="field-body-ref"></a>
## `body/ref`

- Required: `no`
- Shape: string

<a id="field-body-input"></a>
## `body/input`

- Required: `no`
- Shape: unspecified

Transient producer input used only for validation, action rendering context, or digesting. It MUST NOT be persisted by the notification store.

<a id="field-actions"></a>
## `actions`

- Required: `no`
- Shape: array

## Definition Semantics

<a id="def-priority"></a>
## `$defs.priority`

- Shape: enum: `low`, `medium`, `high`

<a id="def-recipientclass"></a>
## `$defs.recipientClass`

- Shape: enum: `operator`, `user`, `pod-user`, `role`

<a id="def-action"></a>
## `$defs.action`

- Shape: object
