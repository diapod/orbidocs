# Relationship Class Changed v1

Source schema: [`doc/schemas/relationship-class-changed.v1.schema.json`](../../schemas/relationship-class-changed.v1.schema.json)

Append-only local fact recording a relationship class definition transition.

## Governing Basis

- [`doc/project/40-proposals/065-local-relationship-layer.md`](../../project/40-proposals/065-local-relationship-layer.md)
- [`doc/project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md`](../../project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)
- [`doc/project/50-requirements/requirements-014-resource-opinions.md`](../../project/50-requirements/requirements-014-resource-opinions.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)
- [`doc/project/30-stories/story-008-cool-site-comment.md`](../../project/30-stories/story-008-cool-site-comment.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `relationship-class-changed.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`fact/id`](#field-fact-id) | `yes` | string |  |
| [`class/id`](#field-class-id) | `yes` | ref: `relationship-class.v1.schema.json#/$defs/class_id` |  |
| [`transition`](#field-transition) | `yes` | enum: `created`, `updated`, `archived`, `unarchived` |  |
| [`prior/definition`](#field-prior-definition) | `no` | ref: `relationship-class.v1.schema.json` |  |
| [`next/definition`](#field-next-definition) | `no` | ref: `relationship-class.v1.schema.json` |  |
| [`actor/ref`](#field-actor-ref) | `yes` | string |  |
| [`event/at`](#field-event-at) | `yes` | string |  |
| [`reason/code`](#field-reason-code) | `no` | string |  |
| [`reason/note`](#field-reason-note) | `no` | string |  |
| [`tx/id`](#field-tx-id) | `yes` | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "transition": {
      "const": "created"
    }
  },
  "required": [
    "transition"
  ]
}
```

Then:

```json
{
  "required": [
    "next/definition"
  ],
  "not": {
    "required": [
      "prior/definition"
    ]
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "transition": {
      "const": "updated"
    }
  },
  "required": [
    "transition"
  ]
}
```

Then:

```json
{
  "required": [
    "prior/definition",
    "next/definition"
  ]
}
```

### Rule 3

When:

```json
{
  "properties": {
    "transition": {
      "const": "archived"
    }
  },
  "required": [
    "transition"
  ]
}
```

Then:

```json
{
  "required": [
    "prior/definition",
    "reason/code"
  ],
  "not": {
    "required": [
      "next/definition"
    ]
  }
}
```

### Rule 4

When:

```json
{
  "properties": {
    "transition": {
      "const": "unarchived"
    }
  },
  "required": [
    "transition"
  ]
}
```

Then:

```json
{
  "required": [
    "prior/definition",
    "next/definition",
    "reason/code"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `relationship-class-changed.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-fact-id"></a>
## `fact/id`

- Required: `yes`
- Shape: string

<a id="field-class-id"></a>
## `class/id`

- Required: `yes`
- Shape: ref: `relationship-class.v1.schema.json#/$defs/class_id`

<a id="field-transition"></a>
## `transition`

- Required: `yes`
- Shape: enum: `created`, `updated`, `archived`, `unarchived`

<a id="field-prior-definition"></a>
## `prior/definition`

- Required: `no`
- Shape: ref: `relationship-class.v1.schema.json`

<a id="field-next-definition"></a>
## `next/definition`

- Required: `no`
- Shape: ref: `relationship-class.v1.schema.json`

<a id="field-actor-ref"></a>
## `actor/ref`

- Required: `yes`
- Shape: string

<a id="field-event-at"></a>
## `event/at`

- Required: `yes`
- Shape: string

<a id="field-reason-code"></a>
## `reason/code`

- Required: `no`
- Shape: string

<a id="field-reason-note"></a>
## `reason/note`

- Required: `no`
- Shape: string

<a id="field-tx-id"></a>
## `tx/id`

- Required: `yes`
- Shape: string
