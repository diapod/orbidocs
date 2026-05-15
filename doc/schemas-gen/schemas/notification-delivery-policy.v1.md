# Notification Delivery Policy v1

Source schema: [`doc/schemas/notification-delivery-policy.v1.schema.json`](../../schemas/notification-delivery-policy.v1.schema.json)

Local host policy controlling whether a created notification interrupts, enters the inbox, is deferred, or is suppressed.

## Governing Basis

- [`doc/project/40-proposals/057-user-and-operator-notifications.md`](../../project/40-proposals/057-user-and-operator-notifications.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `no` | const: `notification-delivery-policy.v1` |  |
| [`enabled`](#field-enabled) | `no` | boolean |  |
| [`policy/ref`](#field-policy-ref) | `no` | string |  |
| [`timezone`](#field-timezone) | `no` | string |  |
| [`safety-critical/kinds`](#field-safety-critical-kinds) | `no` | array |  |
| [`disabled/kinds`](#field-disabled-kinds) | `no` | array |  |
| [`quiet-hours`](#field-quiet-hours) | `no` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `no`
- Shape: const: `notification-delivery-policy.v1`

<a id="field-enabled"></a>
## `enabled`

- Required: `no`
- Shape: boolean

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `no`
- Shape: string

<a id="field-timezone"></a>
## `timezone`

- Required: `no`
- Shape: string

<a id="field-safety-critical-kinds"></a>
## `safety-critical/kinds`

- Required: `no`
- Shape: array

<a id="field-disabled-kinds"></a>
## `disabled/kinds`

- Required: `no`
- Shape: array

<a id="field-quiet-hours"></a>
## `quiet-hours`

- Required: `no`
- Shape: object
