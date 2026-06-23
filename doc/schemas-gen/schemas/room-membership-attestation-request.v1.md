# Room Membership Attestation Request v1

Source schema: [`doc/schemas/room-membership-attestation-request.v1.schema.json`](../../schemas/room-membership-attestation-request.v1.schema.json)

Explicit POST request contract for asking a room authority projection to issue a short-lived membership attestation.

## Governing Basis

- [`P070`](../../project/40-proposals/070-room-primitive.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`request/mode`](#field-request-mode) | `yes` | enum: `invitee-first-join`, `member-self`, `authority-roster` |  |
| [`requester/subject`](#field-requester-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`subject`](#field-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`requested/grants`](#field-requested-grants) | `yes` | array |  |
| [`ttl/seconds`](#field-ttl-seconds) | `no` | integer |  |
| [`authorization`](#field-authorization) | `yes` | object |  |
| [`extensions`](#field-extensions) | `no` | ref: `room.v1.schema.json#/$defs/extensions` |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-request-mode"></a>
## `request/mode`

- Required: `yes`
- Shape: enum: `invitee-first-join`, `member-self`, `authority-roster`

<a id="field-requester-subject"></a>
## `requester/subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-subject"></a>
## `subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-requested-grants"></a>
## `requested/grants`

- Required: `yes`
- Shape: array

<a id="field-ttl-seconds"></a>
## `ttl/seconds`

- Required: `no`
- Shape: integer

<a id="field-authorization"></a>
## `authorization`

- Required: `yes`
- Shape: object

<a id="field-extensions"></a>
## `extensions`

- Required: `no`
- Shape: ref: `room.v1.schema.json#/$defs/extensions`
