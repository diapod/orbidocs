# Corpus Task-pack Step Request v1

Source schema: [`doc/schemas/corpus-task-pack-step.request.v1.schema.json`](../../schemas/corpus-task-pack-step.request.v1.schema.json)

A step a task pack's Flow takes in one Corpus query (P094-023d1), through a corpus.task-pack.* host capability. The context is typed. A participant step names the exact turn, Agent and Corpus inference-Flow binding it acts in: evidence preparation, candidate publication and proposal authoring in the Implementer's turn, review authoring in the Reviewer's. A coordinator step acts for the round: reading the position and admitting a closed chain. The request is the operation's own document, checked under its own contract. The Flow grants no role, opens no turn and creates no binding; the host checks every step against current facts and the role it needs.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-step.request.v1` |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`context`](#field-context) | `yes` | unspecified |  |
| [`request`](#field-request) | `no` | object | The operation's request document; absent for a position read. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-step.request.v1`

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-context"></a>
## `context`

- Required: `yes`
- Shape: unspecified

<a id="field-request"></a>
## `request`

- Required: `no`
- Shape: object

The operation's request document; absent for a position read.
