# Agent Inference Terminal Selection v1

Source schema: [`doc/schemas/agent.inference-terminal-selection.v1.schema.json`](../../schemas/agent.inference-terminal-selection.v1.schema.json)

Explicit host-owned selection of one retained final product from an exact Flow-to-Agent binding. Selection grants neither publication nor effect authority.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)
- [`doc/project/60-solutions/047-agent/047-agent.md`](../../project/60-solutions/047-agent/047-agent.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.inference-terminal-selection.v1` |  |
| [`selection/ref`](#field-selection-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`agent/id`](#field-agent-id) | `yes` | ref: `#/$defs/ref` |  |
| [`product/ref`](#field-product-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`product/digest`](#field-product-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`selected/at`](#field-selected-at) | `yes` | string |  |
| [`selected/by`](#field-selected-by) | `yes` | ref: `#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.inference-terminal-selection.v1`

<a id="field-selection-ref"></a>
## `selection/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-product-ref"></a>
## `product/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-product-digest"></a>
## `product/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string

<a id="field-selected-at"></a>
## `selected/at`

- Required: `yes`
- Shape: string

<a id="field-selected-by"></a>
## `selected/by`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string
