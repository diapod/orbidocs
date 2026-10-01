# Corpus Task-pack Position v1

Source schema: [`doc/schemas/corpus-task-pack-position.v1.schema.json`](../../schemas/corpus-task-pack-position.v1.schema.json)

Where a task-pack loop stands, for the pack's Flow to route its next step (P094-023d1): a projection of the loop and the proposals, reviews, Chair decisions and executions recorded for the query. actionable: step may be taken by its role. waiting: the Chair or a run acts first. blocked: step would be next, but a counter is spent or the deadline passed (an operator's renewal lifts a deadline). stopped: the loop takes nothing more. The position authorizes nothing; every step is checked again when it is taken. Evidence names facts by exact ref and digest, never their content; required items all appear, and optional ones beyond 32 are left out, oldest first, and counted.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-position.v1` |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`binding/ref`](#field-binding-ref) | `yes` | string |  |
| [`loop/state`](#field-loop-state) | `yes` | enum: `open`, `deadline-passed`, `stopped` |  |
| [`deadline`](#field-deadline) | `yes` | string |  |
| [`limits`](#field-limits) | `yes` | ref: `corpus-task-pack-loop.v1.schema.json#/$defs/limits` |  |
| [`spent`](#field-spent) | `yes` | ref: `corpus-task-pack-loop.v1.schema.json#/$defs/spent` |  |
| [`status`](#field-status) | `yes` | enum: `actionable`, `waiting`, `blocked`, `stopped` |  |
| [`step`](#field-step) | `no` | object |  |
| [`waiting`](#field-waiting) | `no` | unspecified |  |
| [`blocked`](#field-blocked) | `no` | unspecified |  |
| [`stop`](#field-stop) | `no` | ref: `corpus-task-pack-loop.v1.schema.json#/$defs/stop` |  |
| [`evidence`](#field-evidence) | `yes` | array |  |
| [`evidence/omitted`](#field-evidence-omitted) | `no` | integer |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "status": {
      "const": "actionable"
    }
  }
}
```

Then:

```json
{
  "required": [
    "step"
  ],
  "not": {
    "anyOf": [
      {
        "required": [
          "waiting"
        ]
      },
      {
        "required": [
          "blocked"
        ]
      },
      {
        "required": [
          "stop"
        ]
      }
    ]
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "status": {
      "const": "waiting"
    }
  }
}
```

Then:

```json
{
  "required": [
    "waiting"
  ],
  "not": {
    "anyOf": [
      {
        "required": [
          "step"
        ]
      },
      {
        "required": [
          "blocked"
        ]
      },
      {
        "required": [
          "stop"
        ]
      }
    ]
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "status": {
      "const": "blocked"
    }
  }
}
```

Then:

```json
{
  "required": [
    "blocked"
  ],
  "not": {
    "required": [
      "stop"
    ]
  }
}
```

### Rule 4

When:

```json
{
  "properties": {
    "status": {
      "const": "stopped"
    }
  }
}
```

Then:

```json
{
  "required": [
    "stop"
  ],
  "not": {
    "anyOf": [
      {
        "required": [
          "step"
        ]
      },
      {
        "required": [
          "waiting"
        ]
      },
      {
        "required": [
          "blocked"
        ]
      }
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-position.v1`

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: string

<a id="field-loop-state"></a>
## `loop/state`

- Required: `yes`
- Shape: enum: `open`, `deadline-passed`, `stopped`

<a id="field-deadline"></a>
## `deadline`

- Required: `yes`
- Shape: string

<a id="field-limits"></a>
## `limits`

- Required: `yes`
- Shape: ref: `corpus-task-pack-loop.v1.schema.json#/$defs/limits`

<a id="field-spent"></a>
## `spent`

- Required: `yes`
- Shape: ref: `corpus-task-pack-loop.v1.schema.json#/$defs/spent`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `actionable`, `waiting`, `blocked`, `stopped`

<a id="field-step"></a>
## `step`

- Required: `no`
- Shape: object

<a id="field-waiting"></a>
## `waiting`

- Required: `no`
- Shape: unspecified

<a id="field-blocked"></a>
## `blocked`

- Required: `no`
- Shape: unspecified

<a id="field-stop"></a>
## `stop`

- Required: `no`
- Shape: ref: `corpus-task-pack-loop.v1.schema.json#/$defs/stop`

<a id="field-evidence"></a>
## `evidence`

- Required: `yes`
- Shape: array

<a id="field-evidence-omitted"></a>
## `evidence/omitted`

- Required: `no`
- Shape: integer
