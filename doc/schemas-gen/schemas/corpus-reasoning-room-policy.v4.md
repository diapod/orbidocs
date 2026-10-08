# Corpus Reasoning Room Policy v4

Source schema: [`doc/schemas/corpus-reasoning-room-policy.v4.schema.json`](../../schemas/corpus-reasoning-room-policy.v4.schema.json)

Explicit current-owner Chair mandate. A declared mandate is not authority; hosts revalidate it before new Chair actions. Historical passport credentials are not accepted by this revision.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `4` |  |
| [`query/id`](#field-query-id) | `yes` | ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/query~1id` |  |
| [`room/id`](#field-room-id) | `yes` | ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/room~1id` |  |
| [`exposure`](#field-exposure) | `yes` | ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/exposure` |  |
| [`answer/acceptance`](#field-answer-acceptance) | `yes` | ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/answer~1acceptance` |  |
| [`chair/mode`](#field-chair-mode) | `yes` | ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/chair~1mode` |  |
| [`chair/nym`](#field-chair-nym) | `yes` | ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/chair~1nym` |  |
| [`chair/agent-ref`](#field-chair-agent-ref) | `no` | ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/chair~1agent-ref` |  |
| [`chair-control-policy/ref`](#field-chair-control-policy-ref) | `no` | ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/chair-control-policy~1ref` |  |
| [`chair-control-policy/digest`](#field-chair-control-policy-digest) | `no` | ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/chair-control-policy~1digest` |  |
| [`extension-binding`](#field-extension-binding) | `no` | ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/extension-binding` |  |
| [`quorum/required`](#field-quorum-required) | `yes` | ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/quorum~1required` |  |
| [`tie-break`](#field-tie-break) | `yes` | ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/tie-break` |  |
| [`revocation-policy`](#field-revocation-policy) | `yes` | ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/revocation-policy` |  |
| [`budget`](#field-budget) | `yes` | ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/budget` |  |
| [`access/list`](#field-access-list) | `yes` | ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/access~1list` |  |
| [`created-at`](#field-created-at) | `yes` | ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/created-at` |  |
| [`expires-at`](#field-expires-at) | `yes` | ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/expires-at` |  |
| [`chair/mandate`](#field-chair-mandate) | `yes` | ref: `corpus-chair-mandate.v1.schema.json` |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `4`

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/query~1id`

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/room~1id`

<a id="field-exposure"></a>
## `exposure`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/exposure`

<a id="field-answer-acceptance"></a>
## `answer/acceptance`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/answer~1acceptance`

<a id="field-chair-mode"></a>
## `chair/mode`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/chair~1mode`

<a id="field-chair-nym"></a>
## `chair/nym`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/chair~1nym`

<a id="field-chair-agent-ref"></a>
## `chair/agent-ref`

- Required: `no`
- Shape: ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/chair~1agent-ref`

<a id="field-chair-control-policy-ref"></a>
## `chair-control-policy/ref`

- Required: `no`
- Shape: ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/chair-control-policy~1ref`

<a id="field-chair-control-policy-digest"></a>
## `chair-control-policy/digest`

- Required: `no`
- Shape: ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/chair-control-policy~1digest`

<a id="field-extension-binding"></a>
## `extension-binding`

- Required: `no`
- Shape: ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/extension-binding`

<a id="field-quorum-required"></a>
## `quorum/required`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/quorum~1required`

<a id="field-tie-break"></a>
## `tie-break`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/tie-break`

<a id="field-revocation-policy"></a>
## `revocation-policy`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/revocation-policy`

<a id="field-budget"></a>
## `budget`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/budget`

<a id="field-access-list"></a>
## `access/list`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/access~1list`

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/created-at`

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v3.schema.json#/properties/expires-at`

<a id="field-chair-mandate"></a>
## `chair/mandate`

- Required: `yes`
- Shape: ref: `corpus-chair-mandate.v1.schema.json`
