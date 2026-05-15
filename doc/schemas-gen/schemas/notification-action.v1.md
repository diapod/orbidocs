# Notification Action v1

Source schema: [`doc/schemas/notification-action.v1.schema.json`](../../schemas/notification-action.v1.schema.json)

Operator-visible action descriptor carried by a notification. Actions are schema-shaped widgets, not embedded UI fragments.

## Governing Basis

- [`doc/project/40-proposals/057-user-and-operator-notifications.md`](../../project/40-proposals/057-user-and-operator-notifications.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`action/id`](#field-action-id) | `yes` | string |  |
| [`kind`](#field-kind) | `yes` | enum: `link`, `button`, `confirm`, `text-input`, `single-choice`, `multi-choice` |  |
| [`label`](#field-label) | `yes` | string |  |
| [`description`](#field-description) | `no` | string |  |
| [`method`](#field-method) | `no` | enum: `GET`, `POST` |  |
| [`target/ref`](#field-target-ref) | `no` | string |  |
| [`target/path`](#field-target-path) | `no` | string |  |
| [`action/expires-at`](#field-action-expires-at) | `no` | string |  |
| [`input/schema`](#field-input-schema) | `no` | object |  |
| [`marks/handled`](#field-marks-handled) | `no` | boolean |  |
## Field Semantics

<a id="field-action-id"></a>
## `action/id`

- Required: `yes`
- Shape: string

<a id="field-kind"></a>
## `kind`

- Required: `yes`
- Shape: enum: `link`, `button`, `confirm`, `text-input`, `single-choice`, `multi-choice`

<a id="field-label"></a>
## `label`

- Required: `yes`
- Shape: string

<a id="field-description"></a>
## `description`

- Required: `no`
- Shape: string

<a id="field-method"></a>
## `method`

- Required: `no`
- Shape: enum: `GET`, `POST`

<a id="field-target-ref"></a>
## `target/ref`

- Required: `no`
- Shape: string

<a id="field-target-path"></a>
## `target/path`

- Required: `no`
- Shape: string

<a id="field-action-expires-at"></a>
## `action/expires-at`

- Required: `no`
- Shape: string

<a id="field-input-schema"></a>
## `input/schema`

- Required: `no`
- Shape: object

<a id="field-marks-handled"></a>
## `marks/handled`

- Required: `no`
- Shape: boolean
