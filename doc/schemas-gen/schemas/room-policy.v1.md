# Room Policy v1

Source schema: [`doc/schemas/room-policy.v1.schema.json`](../../schemas/room-policy.v1.schema.json)

Room access, exposure and retention policy referenced by room.v1.

## Governing Basis

- [`P070`](../../project/40-proposals/070-room-primitive.md)
- [`P009`](../../project/40-proposals/009-communication-exposure-modes.md)
- [`P005`](../../project/40-proposals/005-operator-participation-room-policy-profiles.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`policy/id`](#field-policy-id) | `yes` | string |  |
| [`access/closed`](#field-access-closed) | `yes` | boolean |  |
| [`access/list`](#field-access-list) | `yes` | array |  |
| [`exposure`](#field-exposure) | `yes` | enum: `private-to-swarm`, `federation-local`, `cross-federation`, `global` |  |
| [`live/retention`](#field-live-retention) | `yes` | enum: `non-retained`, `member-local-capture-only`, `public-policy-defined` |  |
| [`max/live-message-bytes`](#field-max-live-message-bytes) | `no` | integer |  |
| [`created-at`](#field-created-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `no` | string |  |
| [`extensions`](#field-extensions) | `no` | ref: `room.v1.schema.json#/$defs/extensions` |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-policy-id"></a>
## `policy/id`

- Required: `yes`
- Shape: string

<a id="field-access-closed"></a>
## `access/closed`

- Required: `yes`
- Shape: boolean

<a id="field-access-list"></a>
## `access/list`

- Required: `yes`
- Shape: array

<a id="field-exposure"></a>
## `exposure`

- Required: `yes`
- Shape: enum: `private-to-swarm`, `federation-local`, `cross-federation`, `global`

<a id="field-live-retention"></a>
## `live/retention`

- Required: `yes`
- Shape: enum: `non-retained`, `member-local-capture-only`, `public-policy-defined`

<a id="field-max-live-message-bytes"></a>
## `max/live-message-bytes`

- Required: `no`
- Shape: integer

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `no`
- Shape: string

<a id="field-extensions"></a>
## `extensions`

- Required: `no`
- Shape: ref: `room.v1.schema.json#/$defs/extensions`
