# Operator Effective Policy Inspection Input V1

Source schema: [`doc/schemas/operator-effective-policy-inspection-input.v1.schema.json`](../../schemas/operator-effective-policy-inspection-input.v1.schema.json)

Prompt-free owner-supplied facts for the pure effective-policy inspection projection.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-effective-policy-inspection-input.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`extension`](#field-extension) | `yes` | ref: `operator-extension-inspection.v1.schema.json` |  |
| [`resource/axes`](#field-resource-axes) | `yes` | array |  |
| [`domain/registries`](#field-domain-registries) | `yes` | array |  |
| [`federation`](#field-federation) | `no` | ref: `#/$defs/federation` |  |
| [`sources/unavailable`](#field-sources-unavailable) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`source`](#def-source) | enum: `inquirium-resource-profile`, `agent-registry`, `corpus-registry`, `arca-registry`, `dator-registry`, `inquirium-registry`, `federation` |  |
| [`domain-name`](#def-domain-name) | enum: `agent`, `corpus`, `arca`, `dator`, `inquirium` |  |
| [`axis`](#def-axis) | object |  |
| [`domain`](#def-domain) | object |  |
| [`federation`](#def-federation) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-effective-policy-inspection-input.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-extension"></a>
## `extension`

- Required: `yes`
- Shape: ref: `operator-extension-inspection.v1.schema.json`

<a id="field-resource-axes"></a>
## `resource/axes`

- Required: `yes`
- Shape: array

<a id="field-domain-registries"></a>
## `domain/registries`

- Required: `yes`
- Shape: array

<a id="field-federation"></a>
## `federation`

- Required: `no`
- Shape: ref: `#/$defs/federation`

<a id="field-sources-unavailable"></a>
## `sources/unavailable`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-source"></a>
## `$defs.source`

- Shape: enum: `inquirium-resource-profile`, `agent-registry`, `corpus-registry`, `arca-registry`, `dator-registry`, `inquirium-registry`, `federation`

<a id="def-domain-name"></a>
## `$defs.domain-name`

- Shape: enum: `agent`, `corpus`, `arca`, `dator`, `inquirium`

<a id="def-axis"></a>
## `$defs.axis`

- Shape: object

<a id="def-domain"></a>
## `$defs.domain`

- Shape: object

<a id="def-federation"></a>
## `$defs.federation`

- Shape: object
