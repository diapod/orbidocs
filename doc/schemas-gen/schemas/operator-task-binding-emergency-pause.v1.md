# Operator Task Binding Emergency Pause v1

Source schema: [`doc/schemas/operator-task-binding-emergency-pause.v1.schema.json`](../../schemas/operator-task-binding-emergency-pause.v1.schema.json)

Request to pause one local binding through the explicit host-local emergency channel. It needs no current operator binding and no expected revision, so losing or revoking the operator binding never takes from the node owner the ability to restrict it. It can only pause: it cannot create, resume, or accept a profile, and it is a separate request on a separate route, never a fallback taken after an ordinary request failed authorization. The transport's host-local authentication is the actor; a binding already paused changes and records nothing.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-binding-emergency-pause.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-binding-emergency-pause.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`
