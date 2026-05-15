# Notification Allow v1

Source schema: [`doc/schemas/notification-allow.v1.schema.json`](../../schemas/notification-allow.v1.schema.json)

Host-side allow policy for external middleware notification authority.

## Governing Basis

- [`doc/project/40-proposals/057-user-and-operator-notifications.md`](../../project/40-proposals/057-user-and-operator-notifications.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`component/id`](#field-component-id) | `yes` | string |  |
| [`notification/kinds`](#field-notification-kinds) | `yes` | array |  |
| [`action/refs`](#field-action-refs) | `no` | array |  |
| [`recipient/classes`](#field-recipient-classes) | `yes` | array |  |
| [`recipient/ids`](#field-recipient-ids) | `no` | array |  |
| [`max/priority`](#field-max-priority) | `yes` | enum: `low`, `medium`, `high` |  |
| [`rate/per-minute`](#field-rate-per-minute) | `no` | integer |  |
| [`redaction/policy/ref`](#field-redaction-policy-ref) | `no` | string |  |
## Field Semantics

<a id="field-component-id"></a>
## `component/id`

- Required: `yes`
- Shape: string

<a id="field-notification-kinds"></a>
## `notification/kinds`

- Required: `yes`
- Shape: array

<a id="field-action-refs"></a>
## `action/refs`

- Required: `no`
- Shape: array

<a id="field-recipient-classes"></a>
## `recipient/classes`

- Required: `yes`
- Shape: array

<a id="field-recipient-ids"></a>
## `recipient/ids`

- Required: `no`
- Shape: array

<a id="field-max-priority"></a>
## `max/priority`

- Required: `yes`
- Shape: enum: `low`, `medium`, `high`

<a id="field-rate-per-minute"></a>
## `rate/per-minute`

- Required: `no`
- Shape: integer

<a id="field-redaction-policy-ref"></a>
## `redaction/policy/ref`

- Required: `no`
- Shape: string
