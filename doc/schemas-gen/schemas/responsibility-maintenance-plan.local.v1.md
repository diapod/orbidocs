# Responsibility-maintenance-plan.local.v1

Source schema: [`doc/schemas/responsibility-maintenance-plan.local.v1.schema.json`](../../schemas/responsibility-maintenance-plan.local.v1.schema.json)

Draft local maintenance contract. Shape validation grants no authority and does not open D7.

## Governing Basis

- [`doc/project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md`](../../project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md)
- [`doc/project/40-proposals/072-capability-registry.md`](../../project/40-proposals/072-capability-registry.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `responsibility-maintenance-plan.local.v1` |  |
| [`command/id`](#field-command-id) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id` |  |
| [`kind`](#field-kind) | `yes` | enum: `prepare`, `abandon`, `verify`, `reconcile`, `compact` |  |
| [`host/id`](#field-host-id) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id` |  |
| [`host/incarnation`](#field-host-incarnation) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id` |  |
| [`operator/binding`](#field-operator-binding) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Binding` |  |
| [`grant`](#field-grant) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Binding` |  |
| [`generation`](#field-generation) | `yes` | unspecified |  |
| [`initial/head`](#field-initial-head) | `yes` | unspecified |  |
| [`source/boundary`](#field-source-boundary) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Boundary` |  |
| [`projector/digest`](#field-projector-digest) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Digest` |  |
| [`verify/mode`](#field-verify-mode) | `yes` | enum: `None`, `integrity`, `archive-publication`, `shadow` |  |
| [`target`](#field-target) | `yes` | enum: `verified`, `abandoned`, `archive-verified`, `compacted`, `reconciled`, `shadow-compared` |  |
| [`deadline/at`](#field-deadline-at) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Time` |  |
| [`budget`](#field-budget) | `yes` | object |  |
| [`storage/transition`](#field-storage-transition) | `yes` | enum: `none`, `2-to-4`, `3-to-4` |  |
| [`compatibility`](#field-compatibility) | `yes` | unspecified |  |
| [`safety`](#field-safety) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Safety` |  |
| [`archive/index-root`](#field-archive-index-root) | `no` | unspecified | Exact archive index root for publication; absence means none. |
| [`supersedes`](#field-supersedes) | `no` | unspecified | Explicit prior compaction command for authorized takeover; absence means none. |
| [`shadow/query`](#field-shadow-query) | `no` | object | One bounded observational query; the run pins one host evaluation instant. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "kind": {
      "const": "verify"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "verify/mode": {
      "enum": [
        "integrity",
        "archive-publication",
        "shadow"
      ]
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "verify/mode": {
      "const": "shadow"
    }
  }
}
```

Then:

```json
{
  "required": [
    "shadow/query"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `responsibility-maintenance-plan.local.v1`

<a id="field-command-id"></a>
## `command/id`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id`

<a id="field-kind"></a>
## `kind`

- Required: `yes`
- Shape: enum: `prepare`, `abandon`, `verify`, `reconcile`, `compact`

<a id="field-host-id"></a>
## `host/id`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id`

<a id="field-host-incarnation"></a>
## `host/incarnation`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id`

<a id="field-operator-binding"></a>
## `operator/binding`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Binding`

<a id="field-grant"></a>
## `grant`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Binding`

<a id="field-generation"></a>
## `generation`

- Required: `yes`
- Shape: unspecified

<a id="field-initial-head"></a>
## `initial/head`

- Required: `yes`
- Shape: unspecified

<a id="field-source-boundary"></a>
## `source/boundary`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Boundary`

<a id="field-projector-digest"></a>
## `projector/digest`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Digest`

<a id="field-verify-mode"></a>
## `verify/mode`

- Required: `yes`
- Shape: enum: `None`, `integrity`, `archive-publication`, `shadow`

<a id="field-target"></a>
## `target`

- Required: `yes`
- Shape: enum: `verified`, `abandoned`, `archive-verified`, `compacted`, `reconciled`, `shadow-compared`

<a id="field-deadline-at"></a>
## `deadline/at`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Time`

<a id="field-budget"></a>
## `budget`

- Required: `yes`
- Shape: object

<a id="field-storage-transition"></a>
## `storage/transition`

- Required: `yes`
- Shape: enum: `none`, `2-to-4`, `3-to-4`

<a id="field-compatibility"></a>
## `compatibility`

- Required: `yes`
- Shape: unspecified

<a id="field-safety"></a>
## `safety`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Safety`

<a id="field-archive-index-root"></a>
## `archive/index-root`

- Required: `no`
- Shape: unspecified

Exact archive index root for publication; absence means none.

<a id="field-supersedes"></a>
## `supersedes`

- Required: `no`
- Shape: unspecified

Explicit prior compaction command for authorized takeover; absence means none.

<a id="field-shadow-query"></a>
## `shadow/query`

- Required: `no`
- Shape: object

One bounded observational query; the run pins one host evaluation instant.
