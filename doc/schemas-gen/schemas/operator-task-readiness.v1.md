# Operator Task Readiness v1

Source schema: [`doc/schemas/operator-task-readiness.v1.schema.json`](../../schemas/operator-task-readiness.v1.schema.json)

Prompt-free readiness projection of one local binding. It is not a grant; derived fields follow the closed P094 rules.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-readiness.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`local-binding/digest`](#field-local-binding-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`task-profile/ref`](#field-task-profile-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`task-profile/digest`](#field-task-profile-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`activation/generation`](#field-activation-generation) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/counter` |  |
| [`evaluated-at`](#field-evaluated-at) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/timestamp` |  |
| [`stages`](#field-stages) | `yes` | object |  |
| [`blockers`](#field-blockers) | `yes` | array |  |
| [`advertisement`](#field-advertisement) | `yes` | object |  |
| [`runnable`](#field-runnable) | `yes` | boolean |  |
| [`publishable`](#field-publishable) | `yes` | boolean |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "publishable": {
      "const": true
    }
  }
}
```

Then:

```json
{
  "properties": {
    "runnable": {
      "const": true
    },
    "stages": {
      "properties": {
        "publication": {
          "properties": {
            "state": {
              "const": "ready"
            }
          }
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
    "runnable": {
      "const": true
    }
  }
}
```

Then:

```json
{
  "properties": {
    "stages": {
      "properties": {
        "package": {
          "properties": {
            "state": {
              "enum": [
                "ready",
                "degraded"
              ]
            }
          }
        },
        "binding": {
          "properties": {
            "state": {
              "enum": [
                "ready",
                "degraded"
              ]
            }
          }
        },
        "environment": {
          "properties": {
            "state": {
              "enum": [
                "ready",
                "degraded"
              ]
            }
          }
        },
        "deliberation": {
          "properties": {
            "state": {
              "enum": [
                "ready",
                "degraded"
              ]
            }
          }
        },
        "effects": {
          "properties": {
            "state": {
              "enum": [
                "ready",
                "degraded"
              ]
            }
          }
        },
        "verification": {
          "properties": {
            "state": {
              "enum": [
                "ready",
                "degraded"
              ]
            }
          }
        },
        "rollback": {
          "properties": {
            "state": {
              "enum": [
                "ready",
                "degraded"
              ]
            }
          }
        }
      }
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-readiness.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-local-binding-digest"></a>
## `local-binding/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-task-profile-ref"></a>
## `task-profile/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-task-profile-digest"></a>
## `task-profile/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-activation-generation"></a>
## `activation/generation`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/counter`

<a id="field-evaluated-at"></a>
## `evaluated-at`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/timestamp`

<a id="field-stages"></a>
## `stages`

- Required: `yes`
- Shape: object

<a id="field-blockers"></a>
## `blockers`

- Required: `yes`
- Shape: array

<a id="field-advertisement"></a>
## `advertisement`

- Required: `yes`
- Shape: object

<a id="field-runnable"></a>
## `runnable`

- Required: `yes`
- Shape: boolean

<a id="field-publishable"></a>
## `publishable`

- Required: `yes`
- Shape: boolean
