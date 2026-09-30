# Corpus Task-pack Review Authoring Request v1

Source schema: [`doc/schemas/corpus-task-pack-review.author.request.v1.schema.json`](../../schemas/corpus-task-pack-review.author.request.v1.schema.json)

Request that the reviewer's node build and sign a review from a committed reviewer product (P094-023b). The product's passage must belong to the named reviewer turn and must have read the exact candidate under review as evidence; the verdict and findings come from the product, everything else from admitted facts.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-review.author.request.v1` |  |
| [`proposal/ref`](#field-proposal-ref) | `yes` | string |  |
| [`agent/id`](#field-agent-id) | `yes` | string |  |
| [`agent/product-ref`](#field-agent-product-ref) | `yes` | string |  |
| [`reviewer-turn/id`](#field-reviewer-turn-id) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `no` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-review.author.request.v1`

<a id="field-proposal-ref"></a>
## `proposal/ref`

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

<a id="field-reviewer-turn-id"></a>
## `reviewer-turn/id`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `no`
- Shape: string
