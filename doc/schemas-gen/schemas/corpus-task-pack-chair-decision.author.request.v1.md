# Corpus Task-pack Chair Decision Authoring Request v1

Source schema: [`doc/schemas/corpus-task-pack-chair-decision.author.request.v1.schema.json`](../../schemas/corpus-task-pack-chair-decision.author.request.v1.schema.json)

An explicit Chair decision over one review (P094-023b), made by a current local operator binding on the Chair's node. It admits or refuses exactly the reviewed experiment and grants no effect: every mutation of a run still needs its own HIL approval.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-chair-decision.author.request.v1` |  |
| [`review/ref`](#field-review-ref) | `yes` | string |  |
| [`decision`](#field-decision) | `yes` | enum: `block`, `request-revision`, `admit-reviewed-candidate` |  |
| [`reason/code`](#field-reason-code) | `yes` | string |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `no` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-chair-decision.author.request.v1`

<a id="field-review-ref"></a>
## `review/ref`

- Required: `yes`
- Shape: string

<a id="field-decision"></a>
## `decision`

- Required: `yes`
- Shape: enum: `block`, `request-revision`, `admit-reviewed-candidate`

<a id="field-reason-code"></a>
## `reason/code`

- Required: `yes`
- Shape: string

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `no`
- Shape: string
