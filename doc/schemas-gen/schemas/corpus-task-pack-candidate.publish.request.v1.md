# Corpus Task-pack Candidate Publication Request v1

Source schema: [`doc/schemas/corpus-task-pack-candidate.publish.request.v1.schema.json`](../../schemas/corpus-task-pack-candidate.publish.request.v1.schema.json)

Request to publish a P094 task-pack candidate into a Corpus Room (P094-022b). It names a committed Agent product of the author's retained turn and carries no candidate bytes: the host reads the product, checks that its passage's Corpus inference-Flow binding ties it to exactly this turn (query, Room, participant, role assignment, turn number) and class, and publishes the canonical candidate the product's kept bytes are.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-candidate.publish.request.v1` |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`turn/id`](#field-turn-id) | `yes` | string |  |
| [`author`](#field-author) | `yes` | ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject` |  |
| [`author/node-id`](#field-author-node-id) | `yes` | string |  |
| [`source/peer`](#field-source-peer) | `yes` | string |  |
| [`agent/id`](#field-agent-id) | `yes` | string |  |
| [`agent/product-ref`](#field-agent-product-ref) | `yes` | string |  |
| [`class/key`](#field-class-key) | `yes` | enum: `Public`, `Community`, `Personal` |  |
| [`candidate/ref`](#field-candidate-ref) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-candidate.publish.request.v1`

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: string

<a id="field-turn-id"></a>
## `turn/id`

- Required: `yes`
- Shape: string

<a id="field-author"></a>
## `author`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject`

<a id="field-author-node-id"></a>
## `author/node-id`

- Required: `yes`
- Shape: string

<a id="field-source-peer"></a>
## `source/peer`

- Required: `yes`
- Shape: string

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: string

<a id="field-agent-product-ref"></a>
## `agent/product-ref`

- Required: `yes`
- Shape: string

<a id="field-class-key"></a>
## `class/key`

- Required: `yes`
- Shape: enum: `Public`, `Community`, `Personal`

<a id="field-candidate-ref"></a>
## `candidate/ref`

- Required: `yes`
- Shape: string
