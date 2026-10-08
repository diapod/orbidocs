# Corpus-task-pack-turn.prepare.request.v1

Source schema: [`doc/schemas/corpus-task-pack-turn.prepare.request.v1.schema.json`](../../schemas/corpus-task-pack-turn.prepare.request.v1.schema.json)

Operator choices for one bounded task-pack participant turn. The owner resolves all configuration, current mandate and membership; choices convey no Agent binding or inference authority.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-turn.prepare.request.v1` |  |
| [`query/id`](#field-query-id) | `yes` | unspecified |  |
| [`task-binding/ref`](#field-task-binding-ref) | `yes` | unspecified |  |
| [`role`](#field-role) | `yes` | enum: `implementer`, `reviewer` |  |
| [`participant`](#field-participant) | `yes` | ref: `#/$defs/participant` |  |
| [`agent/profile-ref`](#field-agent-profile-ref) | `yes` | ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/ref` |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | unspecified |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`participant`](#def-participant) | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-turn.prepare.request.v1`

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: unspecified

<a id="field-task-binding-ref"></a>
## `task-binding/ref`

- Required: `yes`
- Shape: unspecified

<a id="field-role"></a>
## `role`

- Required: `yes`
- Shape: enum: `implementer`, `reviewer`

<a id="field-participant"></a>
## `participant`

- Required: `yes`
- Shape: ref: `#/$defs/participant`

<a id="field-agent-profile-ref"></a>
## `agent/profile-ref`

- Required: `yes`
- Shape: ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/ref`

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: unspecified

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-participant"></a>
## `$defs.participant`

- Shape: unspecified
