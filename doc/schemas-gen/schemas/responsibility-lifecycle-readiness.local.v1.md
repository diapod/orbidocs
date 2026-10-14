# Responsibility-lifecycle-readiness.local.v1

Source schema: [`doc/schemas/responsibility-lifecycle-readiness.local.v1.schema.json`](../../schemas/responsibility-lifecycle-readiness.local.v1.schema.json)

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
| [`schema`](#field-schema) | `yes` | const: `responsibility-lifecycle-readiness.local.v1` |  |
| [`host/id`](#field-host-id) | `yes` | string |  |
| [`host/incarnation`](#field-host-incarnation) | `yes` | string |  |
| [`observed-at`](#field-observed-at) | `yes` | string |  |
| [`lifecycle/v2`](#field-lifecycle-v2) | `yes` | boolean |  |
| [`components`](#field-components) | `yes` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "lifecycle/v2": {
      "const": true
    }
  }
}
```

Then:

```json
{
  "properties": {
    "components": {
      "properties": {
        "storage": {
          "const": true
        },
        "composition": {
          "const": true
        },
        "writers": {
          "const": true
        },
        "replay": {
          "const": true
        },
        "receipts": {
          "const": true
        }
      }
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "components": {
      "properties": {
        "storage": {
          "const": true
        },
        "composition": {
          "const": true
        },
        "writers": {
          "const": true
        },
        "replay": {
          "const": true
        },
        "receipts": {
          "const": true
        }
      }
    }
  }
}
```

Then:

```json
{
  "properties": {
    "lifecycle/v2": {
      "const": true
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `responsibility-lifecycle-readiness.local.v1`

<a id="field-host-id"></a>
## `host/id`

- Required: `yes`
- Shape: string

<a id="field-host-incarnation"></a>
## `host/incarnation`

- Required: `yes`
- Shape: string

<a id="field-observed-at"></a>
## `observed-at`

- Required: `yes`
- Shape: string

<a id="field-lifecycle-v2"></a>
## `lifecycle/v2`

- Required: `yes`
- Shape: boolean

<a id="field-components"></a>
## `components`

- Required: `yes`
- Shape: object
