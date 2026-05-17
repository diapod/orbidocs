# Notification Action Result v1

Source schema: [`doc/schemas/notification-action-result.v1.schema.json`](../../schemas/notification-action-result.v1.schema.json)

Result returned after a notification action submission.

## Governing Basis

- [`doc/project/40-proposals/057-user-and-operator-notifications.md`](../../project/40-proposals/057-user-and-operator-notifications.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `notification-action-result.v1` |  |
| [`status`](#field-status) | `yes` | enum: `accepted`, `action-no-longer-available`, `action-target-not-implemented`, `version-conflict`, `replay-rejected`, `invalid-input` |  |
| [`notification/id`](#field-notification-id) | `yes` | string |  |
| [`action/id`](#field-action-id) | `yes` | string |  |
| [`actor/id`](#field-actor-id) | `no` | string |  |
| [`actor/class`](#field-actor-class) | `no` | enum: `operator`, `participant`, `pod-user`, `http-module`, `in-process-module`, `node`, `org` |  |
| [`action/submission-id`](#field-action-submission-id) | `no` | string |  |
| [`version`](#field-version) | `no` | integer |  |
| [`reason/code`](#field-reason-code) | `no` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `notification-action-result.v1`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `accepted`, `action-no-longer-available`, `action-target-not-implemented`, `version-conflict`, `replay-rejected`, `invalid-input`

<a id="field-notification-id"></a>
## `notification/id`

- Required: `yes`
- Shape: string

<a id="field-action-id"></a>
## `action/id`

- Required: `yes`
- Shape: string

<a id="field-actor-id"></a>
## `actor/id`

- Required: `no`
- Shape: string

<a id="field-actor-class"></a>
## `actor/class`

- Required: `no`
- Shape: enum: `operator`, `participant`, `pod-user`, `http-module`, `in-process-module`, `node`, `org`

<a id="field-action-submission-id"></a>
## `action/submission-id`

- Required: `no`
- Shape: string

<a id="field-version"></a>
## `version`

- Required: `no`
- Shape: integer

<a id="field-reason-code"></a>
## `reason/code`

- Required: `no`
- Shape: string
