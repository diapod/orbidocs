# Corpus Task-pack Proposal Authoring Request v1

Source schema: [`doc/schemas/corpus-task-pack-proposal.author.request.v1.schema.json`](../../schemas/corpus-task-pack-proposal.author.request.v1.schema.json)

Request that the solver's node build and sign a typed proposal from a candidate it published (P094-023b). The request names the publication and the target; the host derives query, Room, turn, author, signer, executor, class and idempotency from admitted facts and narrows expiry to the current authority.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-proposal.author.request.v1` |  |
| [`candidate-publication/ref`](#field-candidate-publication-ref) | `yes` | string |  |
| [`target`](#field-target) | `yes` | ref: `corpus-reasoning-experiment-proposal.v2.schema.json#/$defs/task-pack-target` |  |
| [`expires-at`](#field-expires-at) | `no` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-proposal.author.request.v1`

<a id="field-candidate-publication-ref"></a>
## `candidate-publication/ref`

- Required: `yes`
- Shape: string

<a id="field-target"></a>
## `target`

- Required: `yes`
- Shape: ref: `corpus-reasoning-experiment-proposal.v2.schema.json#/$defs/task-pack-target`

<a id="field-expires-at"></a>
## `expires-at`

- Required: `no`
- Shape: string
