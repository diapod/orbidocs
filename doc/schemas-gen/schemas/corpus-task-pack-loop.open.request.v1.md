# Corpus Task-pack Loop Opening Request v1

Source schema: [`doc/schemas/corpus-task-pack-loop.open.request.v1.schema.json`](../../schemas/corpus-task-pack-loop.open.request.v1.schema.json)

Open the bounded experiment loop of one Corpus query (P094-023c) on the node that owns the round, made by a current local operator binding. The host fixes the loop's limits as the meet of the task pack's profile, the named binding and its own hard caps, and its deadline as one wall time from the opening. A loop opens once per query: the same binding again answers the loop, another binding is a conflict.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-loop.open.request.v1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | string |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-loop.open.request.v1`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: string

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: string
