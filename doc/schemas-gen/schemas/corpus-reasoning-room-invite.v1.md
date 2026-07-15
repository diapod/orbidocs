# Corpus Reasoning Room Invite v1

Source schema: [`doc/schemas/corpus-reasoning-room-invite.v1.schema.json`](../../schemas/corpus-reasoning-room-invite.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/60-solutions/036-room/036-room.md`](../../project/60-solutions/036-room/036-room.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`invite/id`](#field-invite-id) | `yes` | string |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`subject`](#field-subject) | `yes` | ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject` |  |
| [`transport`](#field-transport) | `yes` | object |  |
| [`room-policy`](#field-room-policy) | `yes` | ref: `corpus-reasoning-room-policy.v1.schema.json` |  |
| [`membership-attestation`](#field-membership-attestation) | `yes` | ref: `room-membership-attestation.v1.schema.json` |  |
| [`policy/digest`](#field-policy-digest) | `yes` | string |  |
| [`access/list`](#field-access-list) | `yes` | array |  |
| [`grants`](#field-grants) | `yes` | array |  |
| [`recipient/node-id`](#field-recipient-node-id) | `yes` | string |  |
| [`inviter/node-id`](#field-inviter-node-id) | `yes` | string |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-invite-id"></a>
## `invite/id`

- Required: `yes`
- Shape: string

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: string

<a id="field-subject"></a>
## `subject`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject`

<a id="field-transport"></a>
## `transport`

- Required: `yes`
- Shape: object

<a id="field-room-policy"></a>
## `room-policy`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v1.schema.json`

<a id="field-membership-attestation"></a>
## `membership-attestation`

- Required: `yes`
- Shape: ref: `room-membership-attestation.v1.schema.json`

<a id="field-policy-digest"></a>
## `policy/digest`

- Required: `yes`
- Shape: string

<a id="field-access-list"></a>
## `access/list`

- Required: `yes`
- Shape: array

<a id="field-grants"></a>
## `grants`

- Required: `yes`
- Shape: array

<a id="field-recipient-node-id"></a>
## `recipient/node-id`

- Required: `yes`
- Shape: string

<a id="field-inviter-node-id"></a>
## `inviter/node-id`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object
