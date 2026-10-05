# Operator Task Offer Publication v1

Source schema: [`doc/schemas/operator-task-offer-publication.v1.schema.json`](../../schemas/operator-task-offer-publication.v1.schema.json)

Owner projection of exact draft publication and withdrawal. Current dispatch admission is separate from past publication. A BDO handle is never proof of publication or withdrawal completion.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-offer-publication.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`draft`](#field-draft) | `yes` | ref: `operator-task-offer-draft.v1.schema.json` |  |
| [`state`](#field-state) | `yes` | enum: `unpublished`, `pending`, `published`, `withdrawal-pending`, `withdrawn`, `failed` |  |
| [`admissible`](#field-admissible) | `yes` | boolean |  |
| [`local-binding/current-digest`](#field-local-binding-current-digest) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/digest` | Current host-observed binding revision shown for an explicit action. The retained draft still binds its original revision; inspection never silently rewrites it. |
| [`operation/ref`](#field-operation-ref) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`operation/status`](#field-operation-status) | `no` | enum: `pending`, `running`, `completed`, `failed`, `cancelled`, `unknown` |  |
| [`fenced/reason`](#field-fenced-reason) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/refusalCode` |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "admissible"
  ],
  "properties": {
    "admissible": {
      "const": true
    }
  }
}
```

Then:

```json
{
  "required": [
    "operation/ref",
    "operation/status",
    "local-binding/current-digest"
  ],
  "properties": {
    "state": {
      "const": "published"
    },
    "operation/status": {
      "const": "completed"
    }
  },
  "not": {
    "required": [
      "fenced/reason"
    ]
  }
}
```

### Rule 2

When:

```json
{
  "required": [
    "state"
  ],
  "properties": {
    "state": {
      "const": "unpublished"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "admissible": {
      "const": false
    }
  },
  "not": {
    "anyOf": [
      {
        "required": [
          "operation/ref"
        ]
      },
      {
        "required": [
          "operation/status"
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
  "required": [
    "state"
  ],
  "properties": {
    "state": {
      "enum": [
        "pending",
        "published",
        "withdrawal-pending",
        "withdrawn",
        "failed"
      ]
    }
  }
}
```

Then:

```json
{
  "required": [
    "operation/ref",
    "operation/status"
  ]
}
```

### Rule 4

When:

```json
{
  "required": [
    "state"
  ],
  "properties": {
    "state": {
      "enum": [
        "published",
        "withdrawn"
      ]
    }
  }
}
```

Then:

```json
{
  "properties": {
    "operation/status": {
      "const": "completed"
    }
  }
}
```

### Rule 5

When:

```json
{
  "required": [
    "state"
  ],
  "properties": {
    "state": {
      "const": "failed"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "operation/status": {
      "const": "failed"
    },
    "admissible": {
      "const": false
    }
  }
}
```

### Rule 6

When:

```json
{
  "required": [
    "state"
  ],
  "properties": {
    "state": {
      "enum": [
        "pending",
        "withdrawal-pending"
      ]
    }
  }
}
```

Then:

```json
{
  "properties": {
    "operation/status": {
      "enum": [
        "pending",
        "running",
        "unknown"
      ]
    },
    "admissible": {
      "const": false
    }
  }
}
```

### Rule 7

When:

```json
{
  "required": [
    "state"
  ],
  "properties": {
    "state": {
      "const": "withdrawn"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "admissible": {
      "const": false
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-offer-publication.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-draft"></a>
## `draft`

- Required: `yes`
- Shape: ref: `operator-task-offer-draft.v1.schema.json`

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `unpublished`, `pending`, `published`, `withdrawal-pending`, `withdrawn`, `failed`

<a id="field-admissible"></a>
## `admissible`

- Required: `yes`
- Shape: boolean

<a id="field-local-binding-current-digest"></a>
## `local-binding/current-digest`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

Current host-observed binding revision shown for an explicit action. The retained draft still binds its original revision; inspection never silently rewrites it.

<a id="field-operation-ref"></a>
## `operation/ref`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-operation-status"></a>
## `operation/status`

- Required: `no`
- Shape: enum: `pending`, `running`, `completed`, `failed`, `cancelled`, `unknown`

<a id="field-fenced-reason"></a>
## `fenced/reason`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/refusalCode`
