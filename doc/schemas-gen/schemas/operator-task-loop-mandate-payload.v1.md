# Operator-task-loop-mandate-payload.v1

Source schema: [`doc/schemas/operator-task-loop-mandate-payload.v1.schema.json`](../../schemas/operator-task-loop-mandate-payload.v1.schema.json)

Signed, revocable delegation for one already opened loop, including future owner-admitted plans. Exact opening and binding commitments prevent renewal, rebinding or reuse. No publication, identity, configuration or network widening is granted.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`agent/profiles`](#field-agent-profiles) | `yes` | array |  |
| [`schema`](#field-schema) | `yes` | const: `operator-task-loop-mandate-payload.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`loop/query-id`](#field-loop-query-id) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`loop/opening-digest`](#field-loop-opening-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`pins`](#field-pins) | `yes` | object |  |
| [`bounds`](#field-bounds) | `yes` | object |  |
| [`delegate/ref`](#field-delegate-ref) | `yes` | const: `local-executor:task-pack-delegate` |  |
| [`allowed/actions`](#field-allowed-actions) | `yes` | array |  |
| [`valid/from`](#field-valid-from) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/timestamp` |  |
| [`valid/until`](#field-valid-until) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/timestamp` |  |
| [`confirmation/mode`](#field-confirmation-mode) | `yes` | const: `delegated` |  |
## Field Semantics

<a id="field-agent-profiles"></a>
## `agent/profiles`

- Required: `yes`
- Shape: array

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-loop-mandate-payload.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-loop-query-id"></a>
## `loop/query-id`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-loop-opening-digest"></a>
## `loop/opening-digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-pins"></a>
## `pins`

- Required: `yes`
- Shape: object

<a id="field-bounds"></a>
## `bounds`

- Required: `yes`
- Shape: object

<a id="field-delegate-ref"></a>
## `delegate/ref`

- Required: `yes`
- Shape: const: `local-executor:task-pack-delegate`

<a id="field-allowed-actions"></a>
## `allowed/actions`

- Required: `yes`
- Shape: array

<a id="field-valid-from"></a>
## `valid/from`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/timestamp`

<a id="field-valid-until"></a>
## `valid/until`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/timestamp`

<a id="field-confirmation-mode"></a>
## `confirmation/mode`

- Required: `yes`
- Shape: const: `delegated`
