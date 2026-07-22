# Corpus Reasoning Room Policy v2

Source schema: [`doc/schemas/corpus-reasoning-room-policy.v2.schema.json`](../../schemas/corpus-reasoning-room-policy.v2.schema.json)

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/60-solutions/036-room/036-room.md`](../../project/60-solutions/036-room/036-room.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `2` |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`exposure`](#field-exposure) | `yes` | enum: `private-to-swarm`, `federation-local`, `cross-federation`, `global` |  |
| [`answer/acceptance`](#field-answer-acceptance) | `yes` | enum: `chair-signed`, `n-of-m`, `unanimous` |  |
| [`chair/mode`](#field-chair-mode) | `yes` | enum: `requester-appointed`, `elected` |  |
| [`chair/nym`](#field-chair-nym) | `yes` | string |  |
| [`chair/credentials`](#field-chair-credentials) | `yes` | string |  |
| [`chair/agent-ref`](#field-chair-agent-ref) | `no` | string |  |
| [`chair-control-policy/ref`](#field-chair-control-policy-ref) | `yes` | string |  |
| [`chair-control-policy/digest`](#field-chair-control-policy-digest) | `yes` | string |  |
| [`quorum/required`](#field-quorum-required) | `yes` | integer |  |
| [`tie-break`](#field-tie-break) | `yes` | enum: `chair`, `reject` |  |
| [`revocation-policy`](#field-revocation-policy) | `yes` | enum: `chair-or-requester`, `requester-only` |  |
| [`budget`](#field-budget) | `yes` | object |  |
| [`access/list`](#field-access-list) | `yes` | array |  |
| [`created-at`](#field-created-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`room-subject`](#def-room-subject) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `2`

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: string

<a id="field-exposure"></a>
## `exposure`

- Required: `yes`
- Shape: enum: `private-to-swarm`, `federation-local`, `cross-federation`, `global`

<a id="field-answer-acceptance"></a>
## `answer/acceptance`

- Required: `yes`
- Shape: enum: `chair-signed`, `n-of-m`, `unanimous`

<a id="field-chair-mode"></a>
## `chair/mode`

- Required: `yes`
- Shape: enum: `requester-appointed`, `elected`

<a id="field-chair-nym"></a>
## `chair/nym`

- Required: `yes`
- Shape: string

<a id="field-chair-credentials"></a>
## `chair/credentials`

- Required: `yes`
- Shape: string

<a id="field-chair-agent-ref"></a>
## `chair/agent-ref`

- Required: `no`
- Shape: string

<a id="field-chair-control-policy-ref"></a>
## `chair-control-policy/ref`

- Required: `yes`
- Shape: string

<a id="field-chair-control-policy-digest"></a>
## `chair-control-policy/digest`

- Required: `yes`
- Shape: string

<a id="field-quorum-required"></a>
## `quorum/required`

- Required: `yes`
- Shape: integer

<a id="field-tie-break"></a>
## `tie-break`

- Required: `yes`
- Shape: enum: `chair`, `reject`

<a id="field-revocation-policy"></a>
## `revocation-policy`

- Required: `yes`
- Shape: enum: `chair-or-requester`, `requester-only`

<a id="field-budget"></a>
## `budget`

- Required: `yes`
- Shape: object

<a id="field-access-list"></a>
## `access/list`

- Required: `yes`
- Shape: array

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-room-subject"></a>
## `$defs.room-subject`

- Shape: object
