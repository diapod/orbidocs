# Corpus Task-pack Loop Cancellation Request v1

Source schema: [`doc/schemas/corpus-task-pack-loop.cancel.request.v1.schema.json`](../../schemas/corpus-task-pack-loop.cancel.request.v1.schema.json)

Stop a loop, made by a current local operator binding. No new charge and no new effect of an admitted run follows; a run already started is recovered and published, never abandoned. Cancelling a stopped loop answers the loop as it is.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-loop.cancel.request.v1` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-loop.cancel.request.v1`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: string
