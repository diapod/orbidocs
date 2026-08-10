# Node Extension Posture V1

Source schema: [`doc/schemas/node-extension-posture.v1.schema.json`](../../schemas/node-extension-posture.v1.schema.json)

Signed accountable declaration of one build and extension boundary profile. Self-attestation is not proof of the running binary.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `node-extension-posture.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`posture/ref`](#field-posture-ref) | `yes` | string |  |
| [`node/id`](#field-node-id) | `yes` | string |  |
| [`implementation/profile`](#field-implementation-profile) | `yes` | string |  |
| [`build/digest`](#field-build-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`limit-classification/digest`](#field-limit-classification-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`boundary-profile/digest`](#field-boundary-profile-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`baseline/modified`](#field-baseline-modified) | `yes` | boolean |  |
| [`attestation/strength`](#field-attestation-strength) | `yes` | enum: `self-declared`, `reproducible-build`, `measured-boot`, `third-party` |  |
| [`evidence/refs`](#field-evidence-refs) | `yes` | array |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `node-extension-posture.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-posture-ref"></a>
## `posture/ref`

- Required: `yes`
- Shape: string

<a id="field-node-id"></a>
## `node/id`

- Required: `yes`
- Shape: string

<a id="field-implementation-profile"></a>
## `implementation/profile`

- Required: `yes`
- Shape: string

<a id="field-build-digest"></a>
## `build/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-limit-classification-digest"></a>
## `limit-classification/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-boundary-profile-digest"></a>
## `boundary-profile/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-baseline-modified"></a>
## `baseline/modified`

- Required: `yes`
- Shape: boolean

<a id="field-attestation-strength"></a>
## `attestation/strength`

- Required: `yes`
- Shape: enum: `self-declared`, `reproducible-build`, `measured-boot`, `third-party`

<a id="field-evidence-refs"></a>
## `evidence/refs`

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

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
