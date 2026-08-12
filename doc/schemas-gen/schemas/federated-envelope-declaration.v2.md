# Federated Envelope Declaration V2

Source schema: [`doc/schemas/federated-envelope-declaration.v2.schema.json`](../../schemas/federated-envelope-declaration.v2.schema.json)

Signed compatibility projection binding an operator envelope and exact semantic-registry entries. Activation generations are local fencing evidence, not swarm-wide counters.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `federated-envelope-declaration.v2` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `2` |  |
| [`declaration/ref`](#field-declaration-ref) | `yes` | string |  |
| [`node/id`](#field-node-id) | `yes` | string |  |
| [`envelope/ref`](#field-envelope-ref) | `yes` | string |  |
| [`envelope/digest`](#field-envelope-digest) | `yes` | ref: `#/$defs/hex-digest` |  |
| [`profile/digest`](#field-profile-digest) | `yes` | ref: `#/$defs/hex-digest` |  |
| [`posture/ref`](#field-posture-ref) | `yes` | string |  |
| [`posture/digest`](#field-posture-digest) | `yes` | ref: `#/$defs/hex-digest` |  |
| [`registry/bindings`](#field-registry-bindings) | `yes` | array |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`hex-digest`](#def-hex-digest) | string |  |
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `federated-envelope-declaration.v2`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `2`

<a id="field-declaration-ref"></a>
## `declaration/ref`

- Required: `yes`
- Shape: string

<a id="field-node-id"></a>
## `node/id`

- Required: `yes`
- Shape: string

<a id="field-envelope-ref"></a>
## `envelope/ref`

- Required: `yes`
- Shape: string

<a id="field-envelope-digest"></a>
## `envelope/digest`

- Required: `yes`
- Shape: ref: `#/$defs/hex-digest`

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: ref: `#/$defs/hex-digest`

<a id="field-posture-ref"></a>
## `posture/ref`

- Required: `yes`
- Shape: string

<a id="field-posture-digest"></a>
## `posture/digest`

- Required: `yes`
- Shape: ref: `#/$defs/hex-digest`

<a id="field-registry-bindings"></a>
## `registry/bindings`

- Required: `yes`
- Shape: array

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

## Definition Semantics

<a id="def-hex-digest"></a>
## `$defs.hex-digest`

- Shape: string

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
