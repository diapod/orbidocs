# Agent External Runtime Binding v1

Source schema: [`doc/schemas/agent.external-runtime.binding.v1.schema.json`](../../schemas/agent.external-runtime.binding.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.external-runtime.binding.v1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`binding/digest`](#field-binding-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`agent/id`](#field-agent-id) | `yes` | ref: `#/$defs/ref` |  |
| [`agent-binding/ref`](#field-agent-binding-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`profile/ref`](#field-profile-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`profile/generation`](#field-profile-generation) | `yes` | ref: `#/$defs/positive-safe-integer` |  |
| [`adapter-instance/epoch`](#field-adapter-instance-epoch) | `yes` | ref: `#/$defs/ref` |  |
| [`max/passages`](#field-max-passages) | `yes` | integer |  |
| [`prompt-policy/refs`](#field-prompt-policy-refs) | `yes` | ref: `#/$defs/ref-set` |  |
| [`output-schema/refs`](#field-output-schema-refs) | `yes` | ref: `#/$defs/ref-set` |  |
| [`visibility/ceiling`](#field-visibility-ceiling) | `yes` | enum: `private`, `operator`, `shared` |  |
| [`classification/ceiling`](#field-classification-ceiling) | `yes` | enum: `Public`, `Community`, `Personal` |  |
| [`budget/turn-ceiling`](#field-budget-turn-ceiling) | `yes` | ref: `#/$defs/finite-budget` |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`created/at`](#field-created-at) | `yes` | string |  |
| [`created/by`](#field-created-by) | `yes` | ref: `#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`positive-safe-integer`](#def-positive-safe-integer) | integer |  |
| [`ref-set`](#def-ref-set) | array |  |
| [`finite-budget`](#def-finite-budget) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.external-runtime.binding.v1`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-binding-digest"></a>
## `binding/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-agent-binding-ref"></a>
## `agent-binding/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-profile-ref"></a>
## `profile/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-profile-generation"></a>
## `profile/generation`

- Required: `yes`
- Shape: ref: `#/$defs/positive-safe-integer`

<a id="field-adapter-instance-epoch"></a>
## `adapter-instance/epoch`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-max-passages"></a>
## `max/passages`

- Required: `yes`
- Shape: integer

<a id="field-prompt-policy-refs"></a>
## `prompt-policy/refs`

- Required: `yes`
- Shape: ref: `#/$defs/ref-set`

<a id="field-output-schema-refs"></a>
## `output-schema/refs`

- Required: `yes`
- Shape: ref: `#/$defs/ref-set`

<a id="field-visibility-ceiling"></a>
## `visibility/ceiling`

- Required: `yes`
- Shape: enum: `private`, `operator`, `shared`

<a id="field-classification-ceiling"></a>
## `classification/ceiling`

- Required: `yes`
- Shape: enum: `Public`, `Community`, `Personal`

<a id="field-budget-turn-ceiling"></a>
## `budget/turn-ceiling`

- Required: `yes`
- Shape: ref: `#/$defs/finite-budget`

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

<a id="field-created-at"></a>
## `created/at`

- Required: `yes`
- Shape: string

<a id="field-created-by"></a>
## `created/by`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-positive-safe-integer"></a>
## `$defs.positive-safe-integer`

- Shape: integer

<a id="def-ref-set"></a>
## `$defs.ref-set`

- Shape: array

<a id="def-finite-budget"></a>
## `$defs.finite-budget`

- Shape: object
