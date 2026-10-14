# Responsibility-effect-receipt.v2

Source schema: [`doc/schemas/responsibility-effect-receipt.v2.schema.json`](../../schemas/responsibility-effect-receipt.v2.schema.json)

Draft local contract. Shape validation confers no admission, mandate, application receipt or lifecycle readiness.

## Governing Basis

- [`doc/project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md`](../../project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md)
- [`doc/project/60-solutions/040-capability-limited-restrictions/040-capability-limited-restrictions.md`](../../project/60-solutions/040-capability-limited-restrictions/040-capability-limited-restrictions.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `responsibility-effect-receipt.v2` |  |
| [`host/id`](#field-host-id) | `yes` | string |  |
| [`host/incarnation`](#field-host-incarnation) | `yes` | string |  |
| [`source/id`](#field-source-id) | `yes` | string |  |
| [`request`](#field-request) | `yes` | object |  |
| [`outcome`](#field-outcome) | `yes` | enum: `pending`, `applied`, `suspended`, `resumed`, `retracted`, `refused` |  |
| [`lifecycle`](#field-lifecycle) | `yes` | unspecified |  |
| [`lifecycles`](#field-lifecycles) | `yes` | ref: `responsibility-common.v1.schema.json#/$defs/Binding` |  |
| [`effective-at`](#field-effective-at) | `yes` | string |  |
| [`recorded-at`](#field-recorded-at) | `yes` | string |  |
| [`refusal`](#field-refusal) | `yes` | unspecified |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "outcome": {
      "const": "refused"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "refusal": {
      "enum": [
        "invalid-data",
        "limit-exceeded",
        "actor-mismatch",
        "binding-mismatch",
        "no-authority",
        "stale-revision",
        "case-desynchronized",
        "unsupported-operation",
        "invalid-transition",
        "deadline-elapsed",
        "not-independent",
        "source-set-conflict",
        "source-conflict",
        "retraction-fence",
        "profile-disabled",
        "lifecycle-not-integrated",
        "lifecycle-not-representable-in-v1"
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
    "outcome": {
      "enum": [
        "applied",
        "suspended",
        "resumed",
        "retracted"
      ]
    }
  }
}
```

Then:

```json
{
  "properties": {
    "lifecycle": {
      "$ref": "responsibility-common.v1.schema.json#/$defs/Binding"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `responsibility-effect-receipt.v2`

<a id="field-host-id"></a>
## `host/id`

- Required: `yes`
- Shape: string

<a id="field-host-incarnation"></a>
## `host/incarnation`

- Required: `yes`
- Shape: string

<a id="field-source-id"></a>
## `source/id`

- Required: `yes`
- Shape: string

<a id="field-request"></a>
## `request`

- Required: `yes`
- Shape: object

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: enum: `pending`, `applied`, `suspended`, `resumed`, `retracted`, `refused`

<a id="field-lifecycle"></a>
## `lifecycle`

- Required: `yes`
- Shape: unspecified

<a id="field-lifecycles"></a>
## `lifecycles`

- Required: `yes`
- Shape: ref: `responsibility-common.v1.schema.json#/$defs/Binding`

<a id="field-effective-at"></a>
## `effective-at`

- Required: `yes`
- Shape: string

<a id="field-recorded-at"></a>
## `recorded-at`

- Required: `yes`
- Shape: string

<a id="field-refusal"></a>
## `refusal`

- Required: `yes`
- Shape: unspecified
