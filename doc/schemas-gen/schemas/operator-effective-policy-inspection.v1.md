# Operator Effective Policy Inspection V1

Source schema: [`doc/schemas/operator-effective-policy-inspection.v1.schema.json`](../../schemas/operator-effective-policy-inspection.v1.schema.json)

Cognitively bounded, prompt-free effective-policy read model with stable drill-down refs.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-effective-policy-inspection.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`summary`](#field-summary) | `yes` | ref: `#/$defs/summary` |  |
| [`material/differences`](#field-material-differences) | `yes` | array |  |
| [`domain/registries`](#field-domain-registries) | `yes` | array |  |
| [`federation`](#field-federation) | `no` | ref: `#/$defs/federation` |  |
| [`decisive/restriction`](#field-decisive-restriction) | `no` | ref: `#/$defs/decisive` |  |
| [`drilldown`](#field-drilldown) | `yes` | array |  |
| [`sources/unavailable`](#field-sources-unavailable) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`summary`](#def-summary) | object |  |
| [`difference`](#def-difference) | object |  |
| [`domain`](#def-domain) | object |  |
| [`federation`](#def-federation) | ref: `operator-effective-policy-inspection-input.v1.schema.json#/$defs/federation` |  |
| [`decisive`](#def-decisive) | object |  |
| [`drilldown`](#def-drilldown) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-effective-policy-inspection.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-summary"></a>
## `summary`

- Required: `yes`
- Shape: ref: `#/$defs/summary`

<a id="field-material-differences"></a>
## `material/differences`

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

<a id="field-decisive-restriction"></a>
## `decisive/restriction`

- Required: `no`
- Shape: ref: `#/$defs/decisive`

<a id="field-drilldown"></a>
## `drilldown`

- Required: `yes`
- Shape: array

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

<a id="def-summary"></a>
## `$defs.summary`

- Shape: object

<a id="def-difference"></a>
## `$defs.difference`

- Shape: object

<a id="def-domain"></a>
## `$defs.domain`

- Shape: object

<a id="def-federation"></a>
## `$defs.federation`

- Shape: ref: `operator-effective-policy-inspection-input.v1.schema.json#/$defs/federation`

<a id="def-decisive"></a>
## `$defs.decisive`

- Shape: object

<a id="def-drilldown"></a>
## `$defs.drilldown`

- Shape: object
