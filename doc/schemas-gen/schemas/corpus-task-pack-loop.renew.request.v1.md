# Corpus Task-pack Loop Renewal Request v1

Source schema: [`doc/schemas/corpus-task-pack-loop.renew.request.v1.schema.json`](../../schemas/corpus-task-pack-loop.renew.request.v1.schema.json)

Move the deadline of an unstopped loop later, made by a current local operator binding. Authority never renews itself: this request is the only way a deadline moves. The new deadline lies after the current one and at most one wall time from the renewal. The current deadline again answers the loop.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-loop.renew.request.v1` |  |
| [`deadline`](#field-deadline) | `yes` | string |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-loop.renew.request.v1`

<a id="field-deadline"></a>
## `deadline`

- Required: `yes`
- Shape: string

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: string
