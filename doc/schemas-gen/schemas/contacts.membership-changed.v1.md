# Contacts Membership Changed v1

Source schema: [`doc/schemas/contacts.membership-changed.v1.schema.json`](../../schemas/contacts.membership-changed.v1.schema.json)

Messaging-owned Layer 3 fact recording a change to the local contacts relationship class.

## Governing Basis

- [`doc/project/40-proposals/060-messaging-middleware.md`](../../project/40-proposals/060-messaging-middleware.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `contacts.membership-changed.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`fact/id`](#field-fact-id) | `yes` | string |  |
| [`event/at`](#field-event-at) | `yes` | string |  |
| [`relationship/class`](#field-relationship-class) | `yes` | const: `contacts` |  |
| [`change/kind`](#field-change-kind) | `yes` | enum: `added`, `refreshed`, `removed`, `rotated`, `blocked` |  |
| [`subject`](#field-subject) | `yes` | ref: `#/$defs/subject` |  |
| [`source/ref`](#field-source-ref) | `yes` | string |  |
| [`reason`](#field-reason) | `no` | string |  |
| [`passport/id`](#field-passport-id) | `no` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`subject`](#def-subject) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `contacts.membership-changed.v1`

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

<a id="field-relationship-class"></a>
## `relationship/class`

- Required: `yes`
- Shape: const: `contacts`

<a id="field-change-kind"></a>
## `change/kind`

- Required: `yes`
- Shape: enum: `added`, `refreshed`, `removed`, `rotated`, `blocked`

<a id="field-subject"></a>
## `subject`

- Required: `yes`
- Shape: ref: `#/$defs/subject`

<a id="field-source-ref"></a>
## `source/ref`

- Required: `yes`
- Shape: string

<a id="field-reason"></a>
## `reason`

- Required: `no`
- Shape: string

<a id="field-passport-id"></a>
## `passport/id`

- Required: `no`
- Shape: string

## Definition Semantics

<a id="def-subject"></a>
## `$defs.subject`

- Shape: object
