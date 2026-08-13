# Operator Extension Refusal v1

Source schema: [`doc/schemas/operator-extension-refusal.v1.schema.json`](../../schemas/operator-extension-refusal.v1.schema.json)

Bounded metadata-only diagnostic for one refused extension operation.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-extension-refusal.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`refusal/code`](#field-refusal-code) | `yes` | enum: `contract/unknown-schema`, `hook/unknown`, `hook/version-mismatch`, `offer/digest-mismatch`, `offer/invocation-mismatch`, `decision/not-contained`, `decision/ambiguous`, `decision/unknown-outcome`, `producer/budget-unavailable`, `producer/required-failed`, `producer/output-malformed`, `producer/timeout`, `producer/crash`, `package/signing-authority-untrusted`, `package/digest-mismatch`, `package/conformance-failed`, `package/incompatible`, `activation/plan-stale`, `activation/operator-binding-missing`, `activation/signature-invalid`, `activation/state-conflict`, `activation/session-not-eligible`, `guard/anchor-unknown`, `guard/cap-exceeded`, `identifier/invalid`, `policy/revoked`, `policy/expired`, `extension/safe-mode` |  |
| [`retryable`](#field-retryable) | `yes` | boolean |  |
| [`producer/ref`](#field-producer-ref) | `no` | ref: `#/$defs/ref` |  |
| [`package/ref`](#field-package-ref) | `no` | ref: `#/$defs/ref` |  |
| [`hook/id`](#field-hook-id) | `no` | ref: `#/$defs/field` |  |
| [`hook/v`](#field-hook-v) | `no` | integer |  |
| [`anchor/id`](#field-anchor-id) | `no` | ref: `#/$defs/field` |  |
| [`affected/field`](#field-affected-field) | `no` | ref: `#/$defs/field` |  |
| [`invocation/ref`](#field-invocation-ref) | `no` | ref: `#/$defs/ref` |  |
| [`offer/digest`](#field-offer-digest) | `no` | ref: `#/$defs/digest` |  |
| [`causal/ref`](#field-causal-ref) | `no` | ref: `#/$defs/ref` |  |
| [`declaration/ref`](#field-declaration-ref) | `no` | ref: `#/$defs/ref` |  |
| [`declaration/digest`](#field-declaration-digest) | `no` | ref: `#/$defs/digest` |  |
| [`omitted-producer/refs`](#field-omitted-producer-refs) | `no` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`field`](#def-field) | string |  |
| [`digest`](#def-digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-extension-refusal.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-refusal-code"></a>
## `refusal/code`

- Required: `yes`
- Shape: enum: `contract/unknown-schema`, `hook/unknown`, `hook/version-mismatch`, `offer/digest-mismatch`, `offer/invocation-mismatch`, `decision/not-contained`, `decision/ambiguous`, `decision/unknown-outcome`, `producer/budget-unavailable`, `producer/required-failed`, `producer/output-malformed`, `producer/timeout`, `producer/crash`, `package/signing-authority-untrusted`, `package/digest-mismatch`, `package/conformance-failed`, `package/incompatible`, `activation/plan-stale`, `activation/operator-binding-missing`, `activation/signature-invalid`, `activation/state-conflict`, `activation/session-not-eligible`, `guard/anchor-unknown`, `guard/cap-exceeded`, `identifier/invalid`, `policy/revoked`, `policy/expired`, `extension/safe-mode`

<a id="field-retryable"></a>
## `retryable`

- Required: `yes`
- Shape: boolean

<a id="field-producer-ref"></a>
## `producer/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-package-ref"></a>
## `package/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-hook-id"></a>
## `hook/id`

- Required: `no`
- Shape: ref: `#/$defs/field`

<a id="field-hook-v"></a>
## `hook/v`

- Required: `no`
- Shape: integer

<a id="field-anchor-id"></a>
## `anchor/id`

- Required: `no`
- Shape: ref: `#/$defs/field`

<a id="field-affected-field"></a>
## `affected/field`

- Required: `no`
- Shape: ref: `#/$defs/field`

<a id="field-invocation-ref"></a>
## `invocation/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-offer-digest"></a>
## `offer/digest`

- Required: `no`
- Shape: ref: `#/$defs/digest`

<a id="field-causal-ref"></a>
## `causal/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-declaration-ref"></a>
## `declaration/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-declaration-digest"></a>
## `declaration/digest`

- Required: `no`
- Shape: ref: `#/$defs/digest`

<a id="field-omitted-producer-refs"></a>
## `omitted-producer/refs`

- Required: `no`
- Shape: array

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-field"></a>
## `$defs.field`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string
