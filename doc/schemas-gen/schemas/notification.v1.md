# Notification v1

Source schema: [`doc/schemas/notification.v1.schema.json`](../../schemas/notification.v1.schema.json)

Durable local notification read model. It stores only redacted projections, body/ref, body/text, and digests; raw body/input is intentionally absent.

## Governing Basis

- [`doc/project/40-proposals/057-user-and-operator-notifications.md`](../../project/40-proposals/057-user-and-operator-notifications.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `notification.v1` |  |
| [`notification/id`](#field-notification-id) | `yes` | string |  |
| [`idempotency/key`](#field-idempotency-key) | `no` | string |  |
| [`notification/kind`](#field-notification-kind) | `yes` | string |  |
| [`correlation/id`](#field-correlation-id) | `no` | string |  |
| [`collapse/key`](#field-collapse-key) | `no` | string |  |
| [`supersedes`](#field-supersedes) | `no` | string |  |
| [`version`](#field-version) | `yes` | integer |  |
| [`sender/id`](#field-sender-id) | `yes` | string |  |
| [`recipient/id`](#field-recipient-id) | `yes` | string |  |
| [`recipient/class`](#field-recipient-class) | `yes` | ref: `#/$defs/recipientClass` |  |
| [`subject/ref`](#field-subject-ref) | `no` | string |  |
| [`priority`](#field-priority) | `yes` | ref: `#/$defs/priority` |  |
| [`reason/code`](#field-reason-code) | `yes` | string |  |
| [`delivered/at`](#field-delivered-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `no` | string |  |
| [`snoozed/until`](#field-snoozed-until) | `no` | string |  |
| [`read/opened`](#field-read-opened) | `no` | boolean |  |
| [`handled`](#field-handled) | `no` | boolean |  |
| [`source/component`](#field-source-component) | `no` | string |  |
| [`policy/ref`](#field-policy-ref) | `no` | string |  |
| [`title`](#field-title) | `yes` | string |  |
| [`body/text`](#field-body-text) | `no` | string |  |
| [`body/ref`](#field-body-ref) | `no` | string |  |
| [`body/digest`](#field-body-digest) | `no` | string |  |
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
- Shape: const: `notification.v1`

<a id="field-notification-id"></a>
## `notification/id`

- Required: `yes`
- Shape: string

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `no`
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

<a id="field-supersedes"></a>
## `supersedes`

- Required: `no`
- Shape: string

<a id="field-version"></a>
## `version`

- Required: `yes`
- Shape: integer

<a id="field-sender-id"></a>
## `sender/id`

- Required: `yes`
- Shape: string

<a id="field-recipient-id"></a>
## `recipient/id`

- Required: `yes`
- Shape: string

<a id="field-recipient-class"></a>
## `recipient/class`

- Required: `yes`
- Shape: ref: `#/$defs/recipientClass`

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

<a id="field-delivered-at"></a>
## `delivered/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `no`
- Shape: string

<a id="field-snoozed-until"></a>
## `snoozed/until`

- Required: `no`
- Shape: string

<a id="field-read-opened"></a>
## `read/opened`

- Required: `no`
- Shape: boolean

<a id="field-handled"></a>
## `handled`

- Required: `no`
- Shape: boolean

<a id="field-source-component"></a>
## `source/component`

- Required: `no`
- Shape: string

<a id="field-policy-ref"></a>
## `policy/ref`

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

<a id="field-body-digest"></a>
## `body/digest`

- Required: `no`
- Shape: string

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
