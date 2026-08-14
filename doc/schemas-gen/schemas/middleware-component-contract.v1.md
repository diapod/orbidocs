# Middleware Component Contract v1

Source schema: [`doc/schemas/middleware-component-contract.v1.schema.json`](../../schemas/middleware-component-contract.v1.schema.json)

Transport-neutral dependency and recovery-semantics declaration for one supervised middleware component.

## Governing Basis

- [`doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`](../../project/40-proposals/080-multiplexed-middleware-channel-executor.md)
- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `middleware-component-contract.v1` |  |
| [`component/id`](#field-component-id) | `yes` | ref: `#/$defs/ref` |  |
| [`provides`](#field-provides) | `yes` | array |  |
| [`requires`](#field-requires) | `yes` | array |  |
| [`effects`](#field-effects) | `yes` | object | Effect declarations keyed by their unique effect/id. Ownership is inherited from the enclosing component/id. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string | Non-empty reference composed only of visible ASCII characters. |
| [`digest`](#def-digest) | string |  |
| [`providedContract`](#def-providedcontract) | object |  |
| [`requiredContract`](#def-requiredcontract) | object |  |
| [`effect`](#def-effect) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `middleware-component-contract.v1`

<a id="field-component-id"></a>
## `component/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-provides"></a>
## `provides`

- Required: `yes`
- Shape: array

<a id="field-requires"></a>
## `requires`

- Required: `yes`
- Shape: array

<a id="field-effects"></a>
## `effects`

- Required: `yes`
- Shape: object

Effect declarations keyed by their unique effect/id. Ownership is inherited from the enclosing component/id.

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

Non-empty reference composed only of visible ASCII characters.

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-providedcontract"></a>
## `$defs.providedContract`

- Shape: object

<a id="def-requiredcontract"></a>
## `$defs.requiredContract`

- Shape: object

<a id="def-effect"></a>
## `$defs.effect`

- Shape: object
