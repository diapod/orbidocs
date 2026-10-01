# Corpus Task-pack Chain Admission Request v1

Source schema: [`doc/schemas/corpus-task-pack-chain.admit.request.v1.schema.json`](../../schemas/corpus-task-pack-chain.admit.request.v1.schema.json)

A coordinator step (P094-023d1): admit the experiment of one recorded proposal, closed by the named Chair decision over its recorded review. The host assembles the chain from the Room documents it recorded and admits it as the experiment route does. Admission grants no HIL approval and no access to the Workbench.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-chain.admit.request.v1` |  |
| [`proposal/ref`](#field-proposal-ref) | `yes` | string |  |
| [`decision/ref`](#field-decision-ref) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-chain.admit.request.v1`

<a id="field-proposal-ref"></a>
## `proposal/ref`

- Required: `yes`
- Shape: string

<a id="field-decision-ref"></a>
## `decision/ref`

- Required: `yes`
- Shape: string
