# Operator Task Profile v1

Source schema: [`doc/schemas/operator-task-profile.v1.schema.json`](../../schemas/operator-task-profile.v1.schema.json)

Portable, immutable composition contract of one task-pack profile. It carries refs and digests only: no secrets, machine-local paths, live endpoints, signatures, grants, shell text, or egress instructions.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-profile.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`profile/ref`](#field-profile-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`profile/revision`](#field-profile-revision) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/counter` |  |
| [`thematic-profile`](#field-thematic-profile) | `yes` | object |  |
| [`catalog`](#field-catalog) | `yes` | object |  |
| [`deliberation`](#field-deliberation) | `yes` | object |  |
| [`environment`](#field-environment) | `yes` | object |  |
| [`workbench`](#field-workbench) | `yes` | object |  |
| [`interfaces`](#field-interfaces) | `yes` | object |  |
| [`experiment`](#field-experiment) | `yes` | object |  |
| [`verifier`](#field-verifier) | `yes` | object |  |
| [`rollback`](#field-rollback) | `yes` | object |  |
| [`required-capability/ids`](#field-required-capability-ids) | `yes` | array |  |
| [`resource-envelope/ref`](#field-resource-envelope-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`resource-envelope/digest`](#field-resource-envelope-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`refusal-corpus/ref`](#field-refusal-corpus-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`refusal-corpus/digest`](#field-refusal-corpus-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-profile.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-profile-ref"></a>
## `profile/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-profile-revision"></a>
## `profile/revision`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/counter`

<a id="field-thematic-profile"></a>
## `thematic-profile`

- Required: `yes`
- Shape: object

<a id="field-catalog"></a>
## `catalog`

- Required: `yes`
- Shape: object

<a id="field-deliberation"></a>
## `deliberation`

- Required: `yes`
- Shape: object

<a id="field-environment"></a>
## `environment`

- Required: `yes`
- Shape: object

<a id="field-workbench"></a>
## `workbench`

- Required: `yes`
- Shape: object

<a id="field-interfaces"></a>
## `interfaces`

- Required: `yes`
- Shape: object

<a id="field-experiment"></a>
## `experiment`

- Required: `yes`
- Shape: object

<a id="field-verifier"></a>
## `verifier`

- Required: `yes`
- Shape: object

<a id="field-rollback"></a>
## `rollback`

- Required: `yes`
- Shape: object

<a id="field-required-capability-ids"></a>
## `required-capability/ids`

- Required: `yes`
- Shape: array

<a id="field-resource-envelope-ref"></a>
## `resource-envelope/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-resource-envelope-digest"></a>
## `resource-envelope/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-refusal-corpus-ref"></a>
## `refusal-corpus/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-refusal-corpus-digest"></a>
## `refusal-corpus/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`
