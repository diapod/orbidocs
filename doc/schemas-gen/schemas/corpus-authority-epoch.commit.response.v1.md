# Retained and Activated Communication Epoch v1

Source schema: [`doc/schemas/corpus-authority-epoch.commit.response.v1.schema.json`](../../schemas/corpus-authority-epoch.commit.response.v1.schema.json)

The exact signed transition is retained before creating its Room. Activation does not issue invitations, open a loop, renew its deadline or authorize effects. Those remain separate owner operations.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-authority-epoch.commit.response.v1` |  |
| [`epoch`](#field-epoch) | `yes` | ref: `corpus-authority-epoch.v1.schema.json` |  |
| [`approved/digest`](#field-approved-digest) | `yes` | ref: `corpus-authority-epoch.v1.schema.json#/$defs/digest` |  |
| [`replayed`](#field-replayed) | `yes` | boolean |  |
| [`query/id`](#field-query-id) | `yes` | ref: `corpus-authority-epoch.v1.schema.json#/$defs/query` |  |
| [`room/id`](#field-room-id) | `yes` | ref: `corpus-authority-epoch.v1.schema.json#/$defs/room` |  |
| [`participants/ready`](#field-participants-ready) | `yes` | const: `False` |  |
| [`loop/opened`](#field-loop-opened) | `yes` | const: `False` |  |
| [`effects/authorized`](#field-effects-authorized) | `yes` | const: `False` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-authority-epoch.commit.response.v1`

<a id="field-epoch"></a>
## `epoch`

- Required: `yes`
- Shape: ref: `corpus-authority-epoch.v1.schema.json`

<a id="field-approved-digest"></a>
## `approved/digest`

- Required: `yes`
- Shape: ref: `corpus-authority-epoch.v1.schema.json#/$defs/digest`

<a id="field-replayed"></a>
## `replayed`

- Required: `yes`
- Shape: boolean

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: ref: `corpus-authority-epoch.v1.schema.json#/$defs/query`

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: ref: `corpus-authority-epoch.v1.schema.json#/$defs/room`

<a id="field-participants-ready"></a>
## `participants/ready`

- Required: `yes`
- Shape: const: `False`

<a id="field-loop-opened"></a>
## `loop/opened`

- Required: `yes`
- Shape: const: `False`

<a id="field-effects-authorized"></a>
## `effects/authorized`

- Required: `yes`
- Shape: const: `False`
