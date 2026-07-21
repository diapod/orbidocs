# Sensorium Virt Host Request v1

Source schema: [`doc/schemas/sensorium-virt.host.request.v1.schema.json`](../../schemas/sensorium-virt.host.request.v1.schema.json)

Bounded internal request envelope for daemon-owned Sensorium Virt host authority.

## Governing Basis

- [`doc/project/40-proposals/071-sensorium-workbench.md`](../../project/40-proposals/071-sensorium-workbench.md)

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
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-virt.host.request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`operation`](#field-operation) | `yes` | enum: `fixture.prepare`, `vfkit.allocate`, `environment.start`, `environment.inspect`, `environment.drain`, `environment.teardown`, `environment.recover`, `host.reconcile` |  |
| [`payload`](#field-payload) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`fixturePrepare`](#def-fixtureprepare) | object |  |
| [`environmentBinding`](#def-environmentbinding) | object |  |
| [`vfkitAllocate`](#def-vfkitallocate) | object |  |
| [`environmentLimits`](#def-environmentlimits) | object |  |
| [`emptyPayload`](#def-emptypayload) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "operation": {
      "const": "fixture.prepare"
    }
  },
  "required": [
    "operation"
  ]
}
```

Then:

```json
{
  "properties": {
    "payload": {
      "$ref": "#/$defs/fixturePrepare"
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "operation": {
      "const": "vfkit.allocate"
    }
  },
  "required": [
    "operation"
  ]
}
```

Then:

```json
{
  "properties": {
    "payload": {
      "$ref": "#/$defs/vfkitAllocate"
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "operation": {
      "enum": [
        "environment.inspect",
        "environment.start",
        "environment.drain",
        "environment.teardown",
        "environment.recover"
      ]
    }
  },
  "required": [
    "operation"
  ]
}
```

Then:

```json
{
  "properties": {
    "payload": {
      "$ref": "#/$defs/environmentBinding"
    }
  }
}
```

### Rule 4

When:

```json
{
  "properties": {
    "operation": {
      "const": "host.reconcile"
    }
  },
  "required": [
    "operation"
  ]
}
```

Then:

```json
{
  "properties": {
    "payload": {
      "$ref": "#/$defs/emptyPayload"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-virt.host.request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: enum: `fixture.prepare`, `vfkit.allocate`, `environment.start`, `environment.inspect`, `environment.drain`, `environment.teardown`, `environment.recover`, `host.reconcile`

<a id="field-payload"></a>
## `payload`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-fixtureprepare"></a>
## `$defs.fixturePrepare`

- Shape: object

<a id="def-environmentbinding"></a>
## `$defs.environmentBinding`

- Shape: object

<a id="def-vfkitallocate"></a>
## `$defs.vfkitAllocate`

- Shape: object

<a id="def-environmentlimits"></a>
## `$defs.environmentLimits`

- Shape: object

<a id="def-emptypayload"></a>
## `$defs.emptyPayload`

- Shape: object
